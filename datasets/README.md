# Datasets

## E6 custom tasks, v1

| Split | Records | Math / programming / logic | Use |
|---|---:|---|---|
| [Training](e6_custom_v1/train.jsonl) | 1,500 | 500 / 500 / 500 | Fine-tuning |
| [Development](e6_custom_v1/development.jsonl) | 300 | 100 / 100 / 100 | Previously inspected development evaluation |

Start with the [dataset card](e6_custom_v1/README.md). Both files contain gold answers and reference maps; send only `model_inputs()` messages to a model during evaluation. The separate [result evidence](../results/e6_custom_v1/README.md) contains aggregates, not training records or raw model outputs.

```bash
python -B -m datasets.e6_custom_v1.dataset validate
```

Frozen JSONL bytes, scorer semantics and import paths are unchanged by the repository reorganization. The dataset manifest hashes each packaged file, including the separate source-provenance ledger. A validation pass checks supplied records and reference computations; it does not reproduce model accuracy or establish transfer to unfamiliar material.
