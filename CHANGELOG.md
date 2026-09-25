# Changelog

## 0.2.2 - 2026-09-25

- Add task inputs and gold answers for all 1,500 training tasks as a separate limited-disclosure export.
- Preserve the 300-task development JSONL and reported results unchanged.
- Keep method-specific training targets, prompts, reference maps and the executor excluded; label training/development exposure and reproducibility limits.

## 0.2.1 - 2026-09-25

- Narrow the current dataset release to 300 evaluation task inputs and gold answers.
- Remove training records, method-specific prompts, reference maps, executor/scorer code and detailed source/training metadata from the current tree.
- Retain the completed Original/E6 aggregate results, formatting diagnostic and transfer limitation.
- Update documentation and manifests for the evaluation-only schema. Earlier Git commits are not erased by this change.
