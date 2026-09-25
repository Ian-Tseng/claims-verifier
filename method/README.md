# Historical E1 method

This page preserves the earlier E1 pilot. The current E6 method uses signed cardinalities, indexed relations and finite-set logic, with fixed update100 and a separate development cohort; see the [E6 dataset card](../datasets/e6_custom_v1/README.md) and [current architecture](../architecture.svg). The collector and checkpoint-selection procedure below must not be attributed to E6.

The research goal is to teach a neural network to represent task components and their relationships using symbols. In the pilot, a symbolic map encodes inputs, operations, and a solver in a restricted task language. Task-specific executors check candidate maps and their answers.

## Training flow

1. Start with a procedural task and its public inputs.
2. Generate a candidate symbolic map and answer.
3. Check the candidate using the task executor. When needed, provide an executor-derived corrected target and generate a repaired candidate.
4. Train the model on an accepted map-and-answer target.

The answer-SFT control trains on the answer alone, derived from the same public task oracle. Both arms use Qwen3-8B, 1,500 training tasks, the same task order and initial LoRA weights, and 100 optimizer updates. Each update includes 15 tasks: five per domain. One training seed supplies this pilot.

The collector uses oracle assistance. Of the 1,500 map training tasks, 322 use correction feedback. Verification and correction supervision are part of the evaluated procedure.

## Objective

Let $x_i$ be a task prompt, $a_i$ its answer, and $m_i$ its accepted symbolic map. The target sequence $y_i$ differs between the two arms:

$$
y_i^{\mathrm{answer}}=\operatorname{serialize}(a_i),\qquad
y_i^{\mathrm{map}}=\operatorname{serialize}(m_i,a_i).
$$

For a batch $B$ of 15 tasks, the loss averages over target tokens within each example and then over examples:

$$
\mathcal L(\theta;B)=-\frac{1}{|B|}\sum_{i\in B}\frac{1}{|y_i|}
\sum_{t=1}^{|y_i|}\log p_\theta(y_{i,t}\mid x_i,y_{i,<t}).
$$

Prompt and padding tokens do not contribute to the loss. The map targets contain more tokens than the answer targets. Equal task and update counts therefore do not imply equal supervision tokens or total compute.

## Computational example

For a finite universe $D$, propositions can represent sets of states:

$$
\neg A=D\setminus A,\quad A\land B=A\cap B,\quad A\lor B=A\cup B,
\quad A\rightarrow B=(D\setminus A)\cup B.
$$

An executor can calculate these operations and compare a generated answer with the result. This formal semantics applies to the finite-set logic tasks; it is not a general truth test for natural-language claims.

## Selection and final evaluation

Each arm evaluates checkpoints at updates 20, 40, 60, 80, and 100 on the same 300 development tasks. Selection maximizes final-answer accuracy and takes the earliest update in a tie. The answer-SFT arm selects update 100; the map arm selects update 60.

Final testing uses 1,500 separate tasks and the same prompt and generation budget across arms. The model generates its answer; the evaluator scores it afterward. The pilot does not invoke the map executor to repair answers during test inference. Answer correctness is independent of whether the output contains a valid map. Invalid answer encodings count as incorrect.

The original model and the historical 300-task adapter serve as descriptive references. The primary comparison is the new map arm against the new answer-SFT control.
