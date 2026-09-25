# E6 result evidence

| File | Role |
|---|---|
| [e6_update100_summary.json](e6_update100_summary.json) | E6 fixed-update-100 aggregate: 268/300 correct |
| [matched_comparison.json](matched_comparison.json) | Same-cohort Original/E6 comparison: 69/300 versus 268/300, paired counts and audit scope |
| [logic_wrapper_diagnostic.json](logic_wrapper_diagnostic.json) | Separate post hoc diagnostic: Original 98/300, E6 unchanged; strict scores retained |

Read the [result interpretation](../README.md#result-interpretation) before comparing numbers. These are aggregates from single-seed, previously inspected development evaluations. Raw model responses and checkpoints are not distributed here, so aggregate consistency is not independent scientific replication.

Evaluation task inputs and gold answers are in [datasets/e6_evaluation_v1](../../datasets/e6_evaluation_v1/README.md). A separate [1,500-task training export](../../datasets/e6_training_tasks_v1/README.md) includes task inputs and gold answers only. Complete method-specific training records, prompts, reference maps and the executor remain excluded. File integrity is recorded in the root [release manifest](../../release_manifest.json).
