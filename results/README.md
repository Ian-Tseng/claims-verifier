# Pilot results

The completed procedural pilot compares final-answer accuracy on 1,500 paired test tasks, with 500 tasks each in mathematics, programming, and finite-set logic.

| Model | Correct / tasks | Accuracy |
|---|---:|---:|
| Original Qwen3-8B | 144 / 1,500 | 9.6% |
| Historical 300-task adapter | 154 / 1,500 | 10.3% |
| Answer-SFT, selected update 100 | 325 / 1,500 | 21.7% |
| Verified-map, selected update 60 | 470 / 1,500 | 31.3% |

The primary map-versus-answer-SFT difference is **+9.7 percentage points**, with a paired 95% bootstrap interval of **+7.3 to +12.1 points**. The exact two-sided McNemar test gives $p=9.12\times10^{-10}$, with 352 map-only correct tasks and 207 answer-SFT-only correct tasks. These estimates condition on the selected checkpoints, one training seed, and the sampled task families.

## Results differ by domain

| Domain | Answer-SFT | Verified-map | Difference |
|---|---:|---:|---:|
| Mathematics | 69 / 500 (13.8%) | 199 / 500 (39.8%) | +26.0 pp |
| Programming | 172 / 500 (34.4%) | 56 / 500 (11.2%) | -23.2 pp |
| Finite-set logic | 84 / 500 (16.8%) | 215 / 500 (43.0%) | +26.2 pp |

The best development accuracy is 33.0% (99/300), at map update 60. Development accuracy selects the checkpoint; 31.3% is its final test accuracy.

## Supervision and collection costs

| Quantity | Answer-SFT | Verified-map |
|---|---:|---:|
| Training tasks | 1,500 | 1,500 |
| Optimizer updates | 100 | 100 |
| Supervised target tokens | 22,200 | 136,624 |
| Candidate-generation attempts | 0 | 1,822 |
| Tasks using correction feedback | 0 | 322 |
| Training GPU time | 1,139 s | 1,096 s |
| Candidate-collection GPU time | 0 s | 20,929 s |

Timings cover the recorded training and candidate collection stages, excluding evaluation and model loading. The answer control also uses oracle-derived labels; zero collection attempts means it does not generate candidate maps.

## Interpretation

The result supports the full map-training procedure under this pilot protocol. It does not isolate representation structure from longer targets, oracle-assisted corrections, or collection compute. Programming performance declines, so the overall average does not establish an improvement in every domain.

Strict answer extraction affects scores: the evaluator records 760 answer parse failures for the original model, 708 for the historical adapter, 22 for answer-SFT, and 606 for the map arm. These failures stay in the denominator. The original model's 9.6% score measures this prompt, output contract, and task distribution; it is not a general estimate of Qwen3-8B capability.

This is a single-seed procedural pilot. It does not establish biological plausibility, general natural-language understanding, fact-checking performance, or publication eligibility. Further ablations, seed replication, and external evaluation are necessary to assess those claims.

## Evidence files

- [Machine-readable results](pilot1500.json)
- [Compact benchmark table](pilot1500.csv)
- [Aggregate provenance](provenance.json)

The private experiment stores raw responses, completion records, and source identities. The public snapshot contains aggregate results only, so its hashes support version tracking without providing an independently executable reproduction.
