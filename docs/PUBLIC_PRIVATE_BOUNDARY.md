# Public and private repository boundary

The public repository is `Ian-Tseng/claims-verifier`. It contains only the showcase files listed in the release manifest: descriptions, aggregate results, diagrams, and standalone educational examples.

The core snapshot is prepared for `Ian-Tseng/claims-verifier-core`, a separate private repository. Upload is pending owner confirmation. Do not move the private workspace's Git history into this repository. Never publish checkpoints, model files, full training datasets, raw benchmark responses, local process records, credentials, or internal file paths through this showcase.

Public example code must remain self-contained and clearly labeled as an illustration. No example implies access to a production API or trained model. Private implementation access and any separate commercial terms require an agreement with the repository owner. The public MIT license covers the supplied public files only.

## Updating evidence

1. Complete the private experiment and validate its completion and replay artifacts.
2. Export aggregate counts, denominators, uncertainty, costs, and result scope.
3. Update benchmark status, tables, and the aggregate JSON together.
4. Check the explicit public file list and scan the staged diff for private artifacts before pushing.

The approved introductory wording is retained verbatim in `docs/approved_introduction.md` and the README. Detailed experimental qualifications live in the method and results pages.
