# Public release boundary

The current `Ian-Tseng/claims-verifier` tree includes the files listed in the root release manifest: research descriptions, aggregate results, figures, an educational illustration, and task inputs with gold answers for 1,500 training tasks plus 300 development tasks. This is a **limited-disclosure** release.

Complete method-specific training records and representation targets, method-specific prompts and codebooks, reference maps, the E6 executor/scorer, detailed training configuration, weights, raw model responses and private source ledgers are excluded. Private experiment artifacts remain separate. Any further disclosure requires an explicit scope decision.

The standalone addition demo illustrates a generic operation; it does not implement the E6 method or run a model. The public task-and-answer data reveals task types, difficulty, coverage and expected answers. It supports reuse with separately reported prompts and scoring. Training tasks are not held-out evaluation for E6, and the development tasks were previously inspected. It does not reproduce the exact training or evaluation pipeline.

This boundary describes the current tree. Earlier commits and previously downloaded copies can contain material that has since been removed; removal from the current tree does not establish confidentiality or erase those copies.

## Updating evidence

1. Validate the private experiment's completion and saved outputs.
2. Export approved aggregate counts and their claim limits.
3. Update result text, tables and figures together.
4. Check the explicit public file list and disclosure boundary before publishing.
