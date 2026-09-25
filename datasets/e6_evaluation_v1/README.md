# E6 evaluation tasks and gold answers

This evaluation-only release contains **300 custom development tasks**, with 100 each in mathematics, programming and finite-set logic. It includes task inputs and gold answers only. Training records, method-specific prompts, operator codebooks, reference maps, training configuration and executors are excluded.

| File | Contents |
|---|---|
| [development.jsonl](development.jsonl) | Task IDs, domains, operations, problem descriptions, structured inputs and gold answers |
| [TASKS.md](TASKS.md) | Definitions of the benchmark problems and answer formats |
| [manifest.json](manifest.json) | File hashes, row counts and release scope |

Read the JSONL file with a standard JSON reader. Send only `problem`, `inputs` and the relevant task definition to a model; keep `answer` for scoring. Gold answers are strings for mathematics/programming and objects containing a sorted integer list for logic.

These tasks were previously inspected during development and cover familiar task families. They are not a reserved test of unseen-source transfer. Their task IDs, structured inputs and gold answers match the E6 development cohort, but the method-specific experiment prompts and scorer are not included. Tests using a new prompt or scoring contract are separate evaluations and must not be presented as reproductions of the reported 23.00% versus 89.33% comparison.

The [reported results](../../results/README.md) remain unchanged. This release supports independent testing on the same task content, not reproduction of training or the exact experiment. Record your model, prompts, decoding settings and scoring rule when reporting new results. Cite the repository commit and this manifest hash. The repository's MIT license covers the supplied evaluation materials.

See the [dataset overview](../README.md#what-would-a-training-example-look-like) for a placeholder illustrating the distinction between public evaluation records and private training targets. No real training example is shown.
