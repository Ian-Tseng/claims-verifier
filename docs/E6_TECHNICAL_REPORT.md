# E6: Set-Based Supervision on Custom Reasoning Tasks

Ian-Tseng | Technical report v1 | 25 September 2026 | Development study; not peer reviewed

## Abstract

We evaluate a Qwen3-8B adapter trained to produce computable representations and answers on 1,500 synthetic mathematics, programming and logic tasks. At the fixed update-100 checkpoint, E6 answers 268/300 development tasks correctly (89.33%), compared with Original Qwen3-8B's 69/300 (23.00%) under matched prompts, decoding and strict scoring. Formatting explains part of the difference: a separate post hoc diagnostic recognizes 29 correct Original logic answers missing the required wrapper, raising its diagnostic score to 32.67%. The tasks are previously inspected instances from familiar families. The comparison supports the complete fine-tuning procedure under this protocol; it does not isolate the benefit of set representations.

These results demonstrate improved performance on custom tasks, but a gap remains in transferring that ability to unfamiliar source material.

## Representation and evaluation

E6 uses signed cardinality representations for arithmetic, indexed position/value relations for programming, and operations on subsets of a fixed universe for logic. These constructions preserve quantities, order and repeated values where the task requires them. The complete language is set-based, not powerset-only. A bounded executor checks supported computations, while a task-bound reference contract checks the expected representation. Neither check establishes fidelity to arbitrary natural-language source material.

Each model receives the same task prompt and generates its own response. Final-answer accuracy and reference-contract validity are scored separately after generation. The executor does not repair or replace the model's answer. Correct answers can therefore coexist with invalid maps. The [released dataset](../datasets/e6_custom_v1/README.md) contains the prompts, reference answers and maps, and the frozen executor and scorer.

## Experimental setup

Training contains 1,500 tasks, with 500 per domain. Development contains 300 different instances, with 100 per domain. The development instances were previously inspected; this is not an independent held-out test. E6 starts from Original Qwen3-8B with a fresh LoRA adapter. The fixed final checkpoint follows 100 optimizer updates, one pass through training, using seed 42, learning rate 0.0001, a task batch of 15, microbatch size 1, and a 2,048-token training limit. LoRA uses rank 16, alpha 32 and dropout 0.05. Training uses BF16 and SDPA attention.

The Original control uses the same base revision without an adapter. Evaluation matches ordered task IDs, prompts, codebook, base revision, scorer, greedy decoding, disabled thinking, a 1,024-token generation cap and a 4,096-token context limit. All 600 saved responses passed identity checks and frozen-score replay. This is verification of saved experiment artifacts, not an independent rerun of training or inference. The [protocol](../datasets/e6_custom_v1/protocol.json) and [matched aggregate](../datasets/e6_custom_v1/matched_comparison.json) record configuration and provenance.

## Results

| Domain | Original correct / tasks | E6 correct / tasks |
|---|---:|---:|
| Mathematics | 50/100 | 98/100 |
| Programming | 19/100 | 82/100 |
| Logic, strict output contract | 0/100 | 88/100 |
| **Overall** | **69/300 (23.00%)** | **268/300 (89.33%)** |

Both models answer 69 tasks correctly; 199 are correct only for E6, zero only for Original, and 32 for neither. Original produces 284 JSON-valid outputs and zero reference-contract-valid maps. E6 produces 300 JSON-valid outputs and 267 reference-contract-valid maps. Neither run hits the generation cap. These results concern answer generation and contract compliance within the custom families.

### Formatting diagnostic

Original returns a bare `{"answer": [...]}` object on all 100 logic tasks, rather than the required `{"final_answer": {"answer": [...]}}`. Strict scoring rejects these answers. To distinguish that failure from incorrect answer values, a post hoc rule accepts only bare logic objects containing exactly the `answer` key and a sorted, unique list of exact integers. It changes no values and applies symmetrically to both models; other rows retain their strict scores.

| Scoring view | Original | E6 |
|---|---:|---:|
| Frozen strict scoring | 23.00% | 89.33% |
| Post hoc bare-logic-wrapper diagnostic | 32.67% | 89.33% |

The diagnostic recovers 29 correct Original logic answers. It leaves historical scores unchanged and is not a new independent benchmark. It shows why the strict 0/100 logic result cannot be read as an absence of logical ability. See the [diagnostic rule and counts](../results/logic_wrapper_diagnostic.json).

## Limits and next evaluation

This is a single-seed comparison of an unadapted model with a model receiving additional training. It does not isolate representation choice from training exposure or format learning. The development set covers familiar generated families, has been inspected, and has no expert review. Training-seed stability, independent reproduction and overlap with base-model pretraining remain unestablished. The earlier E1 pilot uses a different cohort and protocol and is not the matched baseline for E6.

These results demonstrate improved performance on custom tasks, but a gap remains in transferring that ability to unfamiliar source material.

The next evaluation should distinguish direct answering, translation from source material into a map, and answering from a checked reference map. A supplied reference map also supplies a plan, so that condition must be reported separately from end-to-end performance. Reserved sources, matched training controls and expert review of source fidelity are needed before claiming improved transfer. This study does not establish that translation is the sole cause of current transfer failures or that a proposed intervention will resolve them.

## Availability

The public v1 release includes the 1,500 training records, 300 development records, reference targets, protocol, aggregate results and reusable validation/scoring utilities. It includes dependency-control targets for reuse, but no completed matched dependency-control training result. It excludes full training infrastructure, model weights and raw model responses. New transfer experiments and collaborator-provided material are outside this release. Dataset validation checks reference computations; it does not reproduce the trained model's accuracy.
