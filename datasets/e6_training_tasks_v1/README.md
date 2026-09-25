# E6 training tasks and gold answers

This **limited-disclosure** release contains the task inputs and gold answers for all **1,500 custom E6 training tasks**: 500 mathematics, 500 programming and 500 finite-set logic tasks.

| File | Contents |
|---|---|
| [train.jsonl](train.jsonl) | Task IDs, domains, operations, problem descriptions, structured inputs and gold answers |
| [manifest.json](manifest.json) | Counts, hashes and disclosure scope |

Each record has exactly `id`, `domain`, `operation`, `problem`, `inputs` and `answer`. See the shared [task definitions](../e6_evaluation_v1/TASKS.md) for answer formats. Use `problem`, `inputs` and the relevant task definition as model input; keep `answer` separate for scoring or use it as a target for your own answer-only training.

These are tasks used to train E6, **not a held-out evaluation set**. E6 accuracy on them cannot establish generalization. The separate [300-task development set](../e6_evaluation_v1/README.md) remains unchanged and was previously inspected; it is not an untouched test of unfamiliar-source transfer.

The records reveal task types, difficulty, coverage and expected answers. They exclude method-specific prompts and codebooks, intermediate maps, representation-training targets, and the E6 executor. They can support task reuse and new training approaches, but do not reproduce E6's representation training or the exact reported evaluation protocol.

"Limited disclosure" does not mean zero disclosure or guaranteed confidentiality. Earlier Git commits and downloaded copies may contain material excluded from the current tree. See the [release boundary](../../docs/PUBLIC_PRIVATE_BOUNDARY.md).

The repository's MIT license covers these supplied task-and-answer records. Cite the repository commit and this manifest when reporting reuse.
