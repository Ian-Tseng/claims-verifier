# Public and private repository boundary

The public repository is `Ian-Tseng/claims-verifier`. It contains the files listed in the release manifest: descriptions, aggregate results, diagrams, standalone educational examples, and the explicitly authorized datasets/e6_custom_v1 release. This dataset exception was authorized on 2026-09-25.

The full training infrastructure, model weights and raw model responses are outside this public release. New transfer work and collaborator-provided material are also excluded. Any further release requires an explicit scope decision. Do not import private Git history, local process records, credentials or internal file paths into this repository.

Public example code must remain self-contained and clearly labeled as an illustration. The E6 dataset utility is separately labeled as an actual bounded executor/scoring contract; it is not the full training pipeline. No example implies access to a production API or trained model. Private implementation access and any separate commercial terms require an agreement with the repository owner. The public MIT license covers the supplied public files only.

## Updating evidence

1. Complete the private experiment and validate its completion and replay artifacts.
2. Export aggregate counts, denominators, uncertainty, costs, and result scope.
3. Update benchmark status, tables, and the aggregate JSON together.
4. Check the explicit public file list and scan the staged diff for private artifacts before pushing.

The README, results page and E6 technical report describe the current matched custom-task comparison and its limitations.
