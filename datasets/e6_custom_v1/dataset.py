"""Standard-library loader and frozen E6 scoring contract; Python 3.10+."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import math
from . import ir

HERE = Path(__file__).resolve().parent
SYSTEM = 'Solve the public task. Return only one JSON object without Markdown.'

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def strict(raw):
    def pairs(kv):
        d={}
        for k,v in kv:
            if k in d:raise ValueError('duplicate_key')
            d[k]=v
        return d
    def bad(x):raise ValueError('nonfinite')
    def number(x):
        v=float(x)
        if not math.isfinite(v):bad(x)
        return v
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad,parse_float=number)

def score(row,raw):
    result={'json_valid':False,'answer_correct':False,'set_map_valid':False,'error':None}
    try:
        doc=strict(raw);result['json_valid']=True
        value=doc['final_answer'];gold=row['answer']
        result['answer_correct']=canonical(value)==canonical(gold)
        if row['public']['task_domain']!='logic':
            try:ir.execute(row['public'],doc);result['set_map_valid']=True
            except (ValueError,KeyError,TypeError,IndexError,OverflowError) as e:result['error']=str(e)[:120]
        else:
            result['set_map_valid']=canonical(doc)==canonical(strict(row['responses']['e6_set']))
    except (ValueError,TypeError,KeyError,IndexError) as e:result['error']=str(e)[:120]
    return result

def render(tokenizer,prompt):
    return tokenizer.apply_chat_template([{'role':'system','content':'Solve the public task. Return only one JSON object without Markdown.'},{'role':'user','content':prompt}],tokenize=False,add_generation_prompt=True,enable_thinking=False)


def load_rows(split='train'):
    """Load labeled records. Never pass complete records to a model."""
    if split not in {'train', 'development'}:
        raise ValueError('split must be train or development')
    with (HERE / (split + '.jsonl')).open(encoding='utf-8') as stream:
        for line in stream:
            yield strict(line)


def model_inputs(split='development'):
    """Yield only task ID and messages, excluding answers and reference maps."""
    for row in load_rows(split):
        yield {'id': row['public']['id'], 'messages': [
            {'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': row['prompt']}]}


def training_examples(arm='e6_set'):
    """Yield the training split as chat messages; target formats stay explicit."""
    if arm not in {'e6_set', 'dependency_control'}:
        raise ValueError('unknown target arm')
    for row in load_rows('train'):
        yield {'id': row['public']['id'], 'messages': [
            {'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': row['prompt']},
            {'role': 'assistant', 'content': row['responses'][arm]}]}


def validate():
    """Verify bytes, population, disjoint identities, and executable references."""
    manifest = strict((HERE / 'manifest.json').read_text(encoding='utf-8'))
    for name, meta in manifest['files'].items():
        path = (HERE / name).resolve()
        if path.parent != HERE.resolve():
            raise ValueError('manifest path outside dataset')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != meta['sha256'] or len(raw) != meta['bytes']:
            raise ValueError('file hash/size mismatch: ' + name)
    seen_ids, seen_tasks, counts = set(), set(), {}
    for split in ('train', 'development'):
        domains = Counter()
        for row in load_rows(split):
            if set(row) != {'public', 'prompt', 'answer', 'responses'}:
                raise ValueError('record schema')
            public = row['public']
            if public['split'] != split or public['id'] in seen_ids or public['task_identity'] in seen_tasks:
                raise ValueError('split or duplicate task identity')
            seen_ids.add(public['id']); seen_tasks.add(public['task_identity'])
            domains[public['task_domain']] += 1
            if not isinstance(row['prompt'], str) or not row['prompt']:
                raise ValueError('prompt')
            if set(row['responses']) != {'e6_set', 'dependency_control'}:
                raise ValueError('target arms')
            for raw in row['responses'].values():
                if canonical(strict(raw)['final_answer']) != canonical(row['answer']):
                    raise ValueError('target answer mismatch')
            result = score(row, row['responses']['e6_set'])
            if not all(result[key] for key in ('json_valid', 'answer_correct', 'set_map_valid')):
                raise ValueError('E6 reference execution: ' + public['id'])
            if public['task_domain'] == 'logic' and canonical(ir.logic_answer(public)) != canonical(row['answer']):
                raise ValueError('logic oracle mismatch')
        if dict(domains) != manifest['domains_per_split'][split] or sum(domains.values()) != manifest['rows'][split]:
            raise ValueError('split population')
        counts[split] = dict(domains)
    return {'state': 'passed', 'rows_verified': len(seen_ids), 'domains': counts,
            'scope': 'Integrity and bounded reference execution; not expert review or unseen-source validation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'example'])
    parser.add_argument('--split', choices=['train', 'development'], default='development')
    args = parser.parse_args()
    print(json.dumps(validate() if args.command == 'validate' else next(model_inputs(args.split)), indent=2))


if __name__ == '__main__':
    main()
