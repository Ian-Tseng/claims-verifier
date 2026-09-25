"""E6 bounded symbolic signed-set and indexed-relation IR. No eval or CUDA."""
import copy,json
CAP=10**9
ROLE={'math':'quantities','programming':'algorithm','logic':'dependencies'}

def integer(x):
    if type(x) is not int or abs(x)>CAP:raise ValueError('bounded_integer')
    return x

def pair(p,n=0):
    integer(p);integer(n)
    if p<0 or n<0:raise ValueError('cardinality_nonnegative')
    # Canonical signed representative, after cancelling equally sized subsets.
    k=min(p,n);return {'p':p-k,'n':n-k}

def encode(x):
    integer(x);return pair(max(x,0),max(-x,0))

def check_pair(x):
    if type(x) is not dict or set(x)!={'p','n'} or pair(x['p'],x['n'])!=x:raise ValueError('signed_set_pair')
    return x

def decode(x):
    x=check_pair(x);return x['p']-x['n']

def pair_union(a,b):
    a=check_pair(a);b=check_pair(b);return pair(a['p']+b['p'],a['n']+b['n'])

def pair_product(a,b):
    a=check_pair(a);b=check_pair(b)
    return pair(a['p']*b['p']+a['n']*b['n'],a['p']*b['n']+a['n']*b['p'])

def relation(x):
    if type(x) is not list or len(x)>128:raise ValueError('indexed_relation')
    ids=[]
    for item in x:
        if type(item) is not list or len(item)!=2 or type(item[0]) is not int or item[0]<0:raise ValueError('indexed_pair')
        ids.append(item[0])
    if ids!=sorted(set(ids)):raise ValueError('unique_ordered_positions')
    return x

def apply(op,args):
    if op=='encode_integer':return encode(args[0])
    if op=='pair_union':return pair_union(*args)
    if op=='pair_difference':return pair_union(args[0],{'p':args[1]['n'],'n':args[1]['p']})
    if op=='pair_product':return pair_product(*args)
    if op=='exact_partition':
        a,b=map(decode,args)
        if b==0 or abs(a)%abs(b):raise ValueError('nonexact_or_zero_partition')
        # Partition the canonical magnitude into blocks of |b|, then apply sign.
        return encode(a//b)
    if op in ('index_values','index_characters'):
        x=args[0]
        if op=='index_values' and type(x) is not list:raise ValueError('sequence_type')
        if op=='index_characters' and (type(x) is not str or not x.isascii()):raise ValueError('ascii_string_required')
        if len(x)>128:raise ValueError('sequence_bound')
        if any(type(v) not in (int,str) for v in x):raise ValueError('sequence_element_type')
        return [[i,v] for i,v in enumerate(x)]
    x=relation(args[0])
    if op in ('select_even','select_positive'):
        for i,v in x:integer(v)
        return [[i,v] for i,v in x if (v%2==0 if op=='select_even' else v>0)]
    if op=='square_values':return [[i,decode(pair_product(encode(v),encode(v)))] for i,v in x]
    if op=='sum_pairs':
        result=encode(0)
        for i,v in x:result=pair_union(result,encode(v))
        return result
    if op=='relation_cardinality':return encode(len(x))
    if op=='first_occurrence':
        seen=set();out=[]
        for i,v in x:
            if v not in seen:seen.add(v);out.append([i,v])
        return out
    if op=='reverse_positions':return [[i,v] for i,(_,v) in enumerate(reversed(x))]
    if op=='uppercase_values':
        if any(type(v) is not str or len(v)!=1 or not v.isascii() for i,v in x):raise ValueError('ascii_character_required')
        return [[i,v.upper()] for i,v in x]
    if op in ('join_pipe','join_characters'):
        if any(type(v) is not str for i,v in x):raise ValueError('string_required')
        return ('|' if op=='join_pipe' else '').join(v for i,v in x)
    raise ValueError('unknown_operator')

def source(public):
    s=public.get('task_spec',public.get('public_inputs'));op=public['operation']
    if public['task_domain']=='math' and 'operands' in s:return {'a':s['operands'][0],'b':s['operands'][1]},op
    return copy.deepcopy(s.get('inputs',s)),op

def skeleton(public):
    inputs,op=source(public);domain=public['task_domain'];steps=[]
    def add(operation,*args):
        ref='s'+str(len(steps)+1);steps.append({'id':ref,'op':operation,'args':list(args)});return ref
    if domain=='math':
        encoded={k:add('encode_integer',k) for k in inputs}
        a=encoded['a'];b=encoded['b']
        if op=='addition':last=add('pair_union',a,b)
        elif op in ('multiplication','rectangle_area'):last=add('pair_product',a,b)
        elif op=='exact_division':last=add('exact_partition',a,b)
        elif op=='multiply_then_add':last=add('pair_union',add('pair_product',a,b),encoded['c'])
        elif op=='sum_then_multiply':last=add('pair_product',add('pair_union',a,b),encoded['c'])
        elif op=='difference_of_products':last=add('pair_difference',add('pair_product',a,b),add('pair_product',encoded['c'],encoded['d']))
        elif op=='square_then_subtract':last=add('pair_difference',add('pair_product',a,a),b)
        else:raise ValueError('unsupported_math_family')
        outputs=[last]
    elif domain=='programming':
        if op=='sum_product':
            x=add('encode_integer','x');y=add('encode_integer','y');outputs=[add('pair_union',x,y),add('pair_product',x,y)]
        elif op=='reverse_uppercase_length':
            x=add('index_characters','text');x=add('reverse_positions',x);x=add('uppercase_values',x);outputs=[add('join_characters',x),add('relation_cardinality',x)]
        else:
            x=add('index_values','values')
            if op=='even_sum_count':x=add('select_even',x)
            elif op=='positive_square_total':x=add('square_values',add('select_positive',x))
            elif op=='unique_preserve_order_join':x=add('first_occurrence',x)
            elif op!='loop_sum_length':raise ValueError('unsupported_program_family')
            outputs=[add('join_pipe' if op=='unique_preserve_order_join' else 'sum_pairs',x),add('relation_cardinality',x)]
    else:raise ValueError('use_legacy_logic_contract')
    return {'kind':'signed_set_relation_v1','inputs':inputs,'steps':steps,'outputs':outputs}

def graph_execute(graph,check_results):
    env=copy.deepcopy(graph['inputs'])
    for step in graph['steps']:
        if step['id'] in env or any(type(k) is not str or k not in env for k in step['args']):raise ValueError('dependency_order')
        value=apply(step['op'],[env[k] for k in step['args']])
        if check_results and json.dumps(step['result'],sort_keys=True,allow_nan=False)!=json.dumps(value,sort_keys=True,allow_nan=False):raise ValueError('forged_step_result')
        env[step['id']]=value
        if not check_results:step['result']=value
    def readout(v):return str(decode(v)) if type(v) is dict else v
    return '\n'.join(readout(env[k]) for k in graph['outputs'])

def logic_answer(public):
    s=public.get('task_spec',public.get('public_inputs'));u=set(s['universe']);op=public['operation']
    values=s.get('sets',s);a=set(values['a']);b=set(values.get('b',[]));z=set(values.get('c',[]))
    if not (a|b|z)<=u:raise ValueError('set_outside_universe')
    if op=='or':v=a|b
    elif op=='not':v=u-a
    elif op=='and':v=a&b
    elif op=='implies':v=(u-a)|b
    elif op=='union_then_intersection':v=(a|b)&z
    elif op=='difference_then_union':v=(a-b)|z
    elif op=='symmetric_difference_then_complement':v=u-(a^b)
    elif op=='implication_then_intersection':v=((u-a)|b)&z
    else:raise ValueError('unsupported_logic')
    return {'answer':sorted(v)}

def reference(public):
    graph=skeleton(public);answer=graph_execute(graph,False)
    return {'component_to_element':{ROLE[public['task_domain']]:graph,'verification':{'answer':answer,'passed':True}},'final_answer':answer}

def execute(public,doc):
    # Strict source binding to this bounded task family; not semantic equivalence.
    if set(doc)!={'component_to_element','final_answer'}:raise ValueError('response_schema')
    mapping=doc['component_to_element'];role=ROLE[public['task_domain']]
    if set(mapping)!={role,'verification'}:raise ValueError('mapping_schema')
    graph=mapping[role];expected=skeleton(public)
    if type(graph) is not dict or set(graph)!=set(expected):raise ValueError('graph_schema')
    if json.dumps(graph['inputs'],sort_keys=True)!=json.dumps(expected['inputs'],sort_keys=True) or graph['outputs']!=expected['outputs'] or graph['kind']!=expected['kind']:raise ValueError('source_binding')
    if len(graph['steps'])!=len(expected['steps']):raise ValueError('step_count')
    for actual,needed in zip(graph['steps'],expected['steps']):
        if set(actual)!=set(needed)|{'result'} or {k:v for k,v in actual.items() if k!='result'}!=needed:raise ValueError('source_operator_binding')
    answer=graph_execute(graph,True)
    verification=mapping['verification']
    if verification!={'answer':answer,'passed':True} or type(verification.get('passed')) is not bool or doc['final_answer']!=answer:raise ValueError('answer_or_verification_mismatch')
    return answer
