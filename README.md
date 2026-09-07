# Claims Verifier

AI research has long debated whether to follow symbolic reasoning or biologically inspired learning mechanisms. We explore how these directions can work together by training neural networks to learn symbolic representations. Our goal is for a network to represent the terms, components, and relationships in a sentence or paragraph using symbols, then generate a structured map that supports logical computation to derive the desired answer.

In this pilot study, we train on verifiable mathematics, programming, and logic tasks. We compare training with verified symbolic maps and answers against supervised fine-tuning that computes loss only on the target answers. On 1,500 held-out tasks, our method achieves 31.3% final-answer accuracy, compared with 21.7% for the answer-only baseline.

We aim to continue training this model on fact-checking and claim-verification datasets using the same symbolic-representation approach. The goal is to represent claims, evidence, and their relationships in maps that support explicit verification.

![Training and evaluation architecture](architecture.png)

## Start here

- [Method and equations](method/README.md): symbolic maps, supervision, and the training/evaluation distinction.
- [Pilot results](results/README.md): aggregate results, domain breakdown, uncertainty, and costs.
- [Benchmark status](benchmarks/README.md): completed procedural testing and the MATH-500 transfer test.
- [Interactive illustration](demo/index.html): download the repository and open this file in a browser.
- [Example usage](example_usage.py): a small, standalone arithmetic-map demonstration.

```bash
python example_usage.py
```

The example and browser demo illustrate symbolic computation. They do not load the trained model or reproduce the pilot.

## Public showcase, private implementation

This repository contains the research overview, aggregate evidence, equations, and educational demonstrations. The model training pipeline, candidate collector, task verifiers, datasets, experiment logs, and trained adapters belong to the private implementation. The core scripts are maintained separately. A private source repository is prepared; its upload is pending owner confirmation.

The public materials support inspection of the approach and its reported results. Full experiment reproduction requires access to the private implementation and artifacts. This repository provides no hosted verification API.

## Research scope

The completed pilot concerns generated mathematics, programming, and finite-set logic tasks. Biological inspiration motivates the research direction; the pilot does not test biological plausibility or establish mastery of arbitrary natural-language claims. The overall gain differs by domain, including lower programming accuracy. See the [result interpretation](results/README.md#interpretation) before drawing broader conclusions.

Fact-checking and claim verification are planned extensions. The project has not yet established performance on those tasks.

## License and citation

The [MIT license](LICENSE) covers the materials supplied in this public repository, including its educational demonstrations. It does not grant access to unpublished implementation or model weights. Third-party models and datasets retain their own licenses. See [CITATION.cff](CITATION.cff) for a repository citation; this project does not claim an accepted paper or DOI.
