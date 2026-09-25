# Claims Verifier

We study whether language models can learn computable representations of a problem and use them to produce verifiable answers. Our goal is to extend this approach to claims and evidence in source material.

E6 is a Qwen3-8B model fine-tuned on **1,500 synthetic math, programming and logic tasks** using set-based representations. At the fixed update-100 checkpoint, it answered **268 of 300 development tasks correctly (89.33%)**. These were separate instances of familiar task families, previously inspected during development. On the same 300 development tasks with matched prompts, decoding and scoring, **Original Qwen3-8B scored 69/300 (23.00%)**, compared with **E6's 268/300 (89.33%)**. Both completed runs passed saved-response identity and score-replay checks.

This result shows performance within the custom task families; reliable transfer to unseen source material remains an open research problem. We are investigating source-to-representation translation, execution and output-format failures separately.

The [dataset and reusable tools](datasets/e6_custom_v1/README.md) include prompts, reference maps, answers, a bounded executor and scoring utilities. The [earlier E1 pilot](results/README.md) is preserved as historical evidence and uses a different evaluation protocol.

```bash
python -B -m datasets.e6_custom_v1.dataset validate
```

![E6 architecture and evaluation boundary](architecture.png)

![E6 development results](figures/e6_results.png)

- [Pilot results](results/README.md): E6 development results and the historical E1 pilot.
- [Benchmark status](benchmarks/README.md): completed evaluations, pending comparisons and transfer limits.
- [Illustration](demo/index.html): a standalone symbolic-computation demo; download and open it in a browser. It does not run the trained model.

## Research scope

The E6 result concerns generated mathematics, programming and finite-set logic tasks. It does not establish mastery of arbitrary natural-language claims. The earlier E1 pilot has separate results and limitations, including a programming decline; see the [result interpretation](results/README.md#result-interpretation) and the separately labeled E1 findings.

This release does not report downstream fact-verification comparisons or establish reliable transfer to unseen sources.

## License and citation

The [MIT license](LICENSE) covers the materials supplied in this public repository, including its educational demonstrations and the E6 synthetic dataset and utilities. The full training pipeline and model weights are not included. Third-party models and datasets retain their own licenses. See [CITATION.cff](CITATION.cff) for a repository citation; this project does not claim an accepted paper or DOI.
