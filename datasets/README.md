# Task inputs and gold answers

This is a **limited-disclosure** release. It publishes task content and expected answers, while withholding method-specific prompts, codebooks, intermediate maps, representation-training targets and the E6 executor.

| Split | Tasks | Per domain | Use |
|---|---:|---:|---|
| [Training](e6_training_tasks_v1/README.md) | 1,500 | 500 | Inspect training coverage or train your own models; not held-out evaluation for E6 |
| [Development](e6_evaluation_v1/README.md) | 300 | 100 | Previously inspected evaluation instances from familiar task families |

Both splits cover mathematics, programming and finite-set logic. Each record contains only `id`, `domain`, `operation`, `problem`, `inputs` and the gold `answer`. Keep gold answers out of model inputs when evaluating. The existing development JSONL and [reported results](../results/README.md) are unchanged.

## Disclosure and reuse

The tasks reveal problem types, difficulty, coverage and answers. This is limited disclosure, not zero exposure or a confidentiality guarantee. Earlier Git commits and downloaded copies may contain removed material; see the [release boundary](../docs/PUBLIC_PRIVATE_BOUNDARY.md).

The 1,500 training-task records are not the complete supervised examples used to train E6. You can use their gold answers for your own training, but the release does not reproduce E6's representation training. E6 performance on its training tasks cannot demonstrate generalization. The 300 development tasks are not an untouched test of unseen-source transfer.

New evaluations must report their model, prompts, decoding and scoring. Sharing task IDs alone does not reproduce the reported comparison because the original method prompts and scorer are withheld. See [task definitions](e6_evaluation_v1/TASKS.md).

## What would a training example look like?

The following is a conceptual placeholder, not an actual method-training record or an executable format:

```text
Input: [task description and inputs]
Training target: [private structured representation] + [gold answer]
```

This shows the broad supervision idea. The actual representation schema, operators, intermediate steps and exact training-output format are not included.
