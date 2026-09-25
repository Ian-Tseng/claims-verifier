# Benchmark status

## E6 release snapshot: 2026-09-25

| Evaluation | Population | State | Evidence boundary |
|---|---|---|---|
| E6 update100 | 300 custom development tasks | Complete: 268/300 (89.33%) | Familiar families, previously inspected, single seed |
| Original matched E6 control | Same 300 tasks and protocol | Complete: 69/300 (23.00%) | Same-cohort comparison; saved-response replay passed |
| Reliable unseen-source transfer | New provided source groups | Not established | No claim of resolved transfer from custom-task accuracy |

See [current pilot results](../results/README.md) and [reusable E6 dataset](../datasets/e6_custom_v1/README.md).

## Historical E1 transfer plan

Status snapshot: 2026-09-07. The table below is historical, not a live monitor. A separate [E6 development dataset release](../datasets/e6_custom_v1/README.md) was added on 2026-09-25; it does not update the historical MATH-500 or fact-verification entries below.

| Benchmark | Tasks | Models | State | Result |
|---|---:|---|---|---|
| Procedural math, programming, and logic | 1,500 test | Original, historical adapter, answer-SFT, verified-map | Complete | [Pilot table](../results/README.md) |
| MATH-500 external transfer | 500 test per model | Original, answer-SFT update 100, verified-map update 60 | In progress | Pending completion and replay |
| Fact-checking / claim verification | To be defined | To be defined | Planned | No results |

## MATH-500 transfer protocol

The external study uses all 500 questions from [HuggingFaceH4/MATH-500](https://huggingface.co/datasets/HuggingFaceH4/MATH-500), revision `6e4ed1a2a79af7d8630a6b768ec859cb5af4d3be`. It evaluates existing checkpoints without retraining or selecting new checkpoints on benchmark outcomes.

All three models receive identical prompts and a 2,048-token output budget in non-thinking mode, using temperature 0.7, top-p 0.8, top-k 20, and one sample per task. Seeds and batches match across arms. A mathematical-equivalence scorer evaluates the final boxed answer or a strict JSON final_answer string. Missing or malformed final answers count as incorrect.

This shared transfer protocol differs from published Qwen benchmark settings. Cross-paper scores do not provide a matched comparison. Base-model pretraining contamination is unknown. We will publish complete aggregate results after all three arms finish and replay checks pass, including any losses relative to the original model or answer-SFT.
