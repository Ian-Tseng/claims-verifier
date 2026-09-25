# Claims Verifier

We study whether language models can learn computable representations of a problem and use them to produce verifiable answers. Our goal is to extend this approach to claims and evidence in source material.

E6 is a Qwen3-8B model fine-tuned on **1,500 synthetic math, programming and logic tasks** using set-based representations. On the same **300 development tasks**, E6 at the fixed update-100 checkpoint scored **89.33% (268/300)**, compared with **23.00% (69/300)** for Original Qwen3-8B, under matched prompts, decoding and strict answer scoring. These are previously inspected instances of familiar task families. Output formatting affects this comparison; see the [result interpretation](results/README.md#result-interpretation).

These results demonstrate improved performance on custom tasks, but a gap remains in transferring that ability to unfamiliar source material.

The [evaluation dataset](datasets/e6_evaluation_v1/README.md) contains 300 task inputs and gold answers for independent testing. Training data, method-specific prompts, reference maps and the executor are excluded. The [technical report](docs/E6_TECHNICAL_REPORT.md) explains the reported comparison and its limitations.

![E6 architecture and evaluation boundary](architecture.png)

![E6 development results](figures/e6_results.png)

- [E6 results](results/README.md): Matched Original/E6 development results.
- [Benchmark status](benchmarks/README.md): completed evaluations, pending comparisons and transfer limits.
- [Illustration](demo/index.html): a standalone symbolic-computation demo; download and open it in a browser. It does not run the trained model.

## Research scope

The E6 result concerns generated mathematics, programming and finite-set logic tasks. It does not establish mastery of arbitrary natural-language claims. See the [result interpretation](results/README.md#result-interpretation) for the output-format diagnostic and limits of the matched comparison.

This release does not report downstream fact-verification comparisons or establish reliable transfer to unseen sources.

## Repository layout

| Folder | Contents |
|---|---|
| [datasets](datasets/README.md) | Evaluation task inputs, gold answers and task definitions |
| [results](results/README.md) | Current E6 comparison, result evidence and interpretation |
| [figures](figures/README.md) | Rendered results and the figure generator; architecture images are at the root |
| [docs](docs/E6_TECHNICAL_REPORT.md) | Technical report and release boundary |
| [demo](demo/index.html) | Standalone educational illustration |

## License and citation

The [MIT license](LICENSE) covers the materials supplied in this public repository, including its educational demonstrations and E6 evaluation data. The full training pipeline and model weights are not included. Third-party models and datasets retain their own licenses. See [CITATION.cff](CITATION.cff) for a repository citation; this project does not claim an accepted paper or DOI.
