# E6 custom math, programming and finite-set logic dataset, v1

This release contains the exact **1,500 training tasks** and **300 development tasks** used in the E6 set-representation experiment, with prompts, answers and two reference target formats. All tasks are procedurally generated synthetic problems. Each split is balanced across mathematics, programming and finite-set logic.

The 300 development tasks use new values or instances of familiar task families. They were repeatedly inspected during development. They are **not an untouched test set, unseen compositions, or evidence of transfer to unfamiliar source material**.

## Quick start

From the repository root, using Python 3.10 or newer (no third-party dependencies):

```bash
python -B -m datasets.e6_custom_v1.dataset validate
python -B -m datasets.e6_custom_v1.dataset example
```

```python
from datasets.e6_custom_v1 import load_rows, model_inputs, training_examples, score

# Evaluation inputs deliberately exclude gold answers and reference maps.
example = next(model_inputs("development"))
messages = example["messages"]  # send only these messages to your model

# For fine-tuning, train-only examples include an assistant target.
training_row = next(training_examples("e6_set"))

# Scoring happens separately, after generating a response.
row = next(load_rows("development"))
raw_response = '{"final_answer":"0"}'  # replace with the model's actual output
print(score(row, raw_response))
```

Run these imports from this repository root to avoid conflicts with an installed package also named `datasets`. Each `responses` value is a JSON-encoded string; parse it once when inspecting its structure. Preserve it as text when constructing a training target. Do not train on the development split or include `answer`/`responses` in evaluation inputs.

## Files and schema

| File / field | Purpose |
|---|---|
| `train.jsonl` | 1,500 records: 500 per domain |
| `development.jsonl` | 300 records: 100 per domain |
| `public` | Task ID, domain, operation, structured source inputs, split and task identity |
| `prompt` | Exact user prompt, including the shared operator codebook |
| `answer` | Canonical gold answer: a string for math/programming, an object for logic |
| `responses.e6_set` | Set/relation-map supervision and final answer |
| `responses.dependency_control` | Matched legacy map target; its inclusion does not imply a completed control training run |
| `ir.py`, `dataset.py` | Bounded executor, frozen scoring functions, loader and release validator |
| `protocol.json` | Training and evaluation settings, with a portable model identifier |
| `manifest.json` | Checksums, sizes, counts, coverage and source provenance |
| `e6_update100_summary.json` | Full 300-row development aggregate for the fixed update-100 checkpoint |

The two JSONL files are byte-identical to the frozen experiment files. Their SHA-256 values are recorded in the manifest. The source-file ledger uses repository-relative paths; it identifies private generator sources without implying those sources are included. Released files use this repository's **MIT license** (see `LICENSE`). This grant covers the supplied synthetic records and utility code; third-party model weights retain their own terms.

## Representation and scoring

E6 is a **set-theoretic intermediate representation**, not powerset-only computation:

- Math uses normalized signed cardinalities (`p - n`), disjoint union, Cartesian products and exact partition for division. Division here has no remainder and requires a nonzero divisor.
- Programming uses indexed relations to preserve positions and repeated values, with bounded operations for filtering, aggregation and string transformations.
- Logic uses subsets of a declared finite universe, with union, intersection, difference and complement. Logic targets are identical across the two supplied formats.

`score` preserves the experiment's distinction between final-answer accuracy and map-contract validity. A correct final answer can score correctly even when its map fails. For math/programming, the executor binds the graph to the source task and checks intermediate values against a specific supported graph structure. It does not recognize every mathematically equivalent program. For logic, map validity requires exact canonical equality with the reference; this is a strict reference contract, not a general semantic equivalence test. The model's `verification.passed` field alone is not independent verification.

The release validator checks both target formats' gold answers and executes every E6 reference. It does not fully execute the legacy dependency-control format. Source provenance records checks against the earlier E5 splits; the standalone validator only checks duplicate IDs and task identities within these two released splits. Base-model pretraining overlap is unknown.

## Recorded E6 result

E6 started from Original Qwen3-8B with a fresh LoRA adapter and trained for 100 updates on the 1,500 training tasks. The checkpoint was fixed at update 100. Evaluation used greedy decoding, non-thinking mode, batch size 1 and a 1,024-new-token cap; see `protocol.json`. To reproduce the chat prefix, `dataset.render(tokenizer, prompt)` applies the frozen system message and `enable_thinking=False`.

| Domain | Correct / development tasks | Accuracy | Reference-contract valid |
|---|---:|---:|---:|
| Math | 98 / 100 | 98.00% | 98 / 100 |
| Programming | 82 / 100 | 82.00% | 82 / 100 |
| Logic | 88 / 100 | 88.00% | 87 / 100 |
| **Total** | **268 / 300** | **89.33%** | **267 / 300** |

All 300 outputs parsed as JSON; none hit the generation cap. This is a single-seed automated development result with zero expert reviews. On the same 300 development tasks with matched prompts, decoding and scoring, **Original Qwen3-8B scored 69/300 (23.00%)**, compared with **E6's 268/300 (89.33%)**. Both completed runs passed saved-response identity and score-replay checks. These results demonstrate improved performance on custom tasks, but a gap remains in transferring that ability to unfamiliar source material.

This package supports task reuse and execution/scoring of supplied targets and new predictions. It does not contain trained adapters, raw model responses, the full generator, or the training pipeline; it is not by itself a complete reproduction of training or the reported model accuracy. The validator cannot independently reproduce an aggregate model result without its predictions and checkpoint.

For reuse, cite the repository's `CITATION.cff`, name `e6_custom_v1`, and record the Git commit and dataset manifest hash. Keep this version immutable in downstream work; publish altered tasks, prompts or scoring rules under a new version and report those changes.

The Original baseline has an output-wrapper failure on all 100 logic tasks. A separately labeled [post hoc diagnostic](../../results/README.md#result-interpretation) recovers 29 correct bare logic answers without changing the strict result.
