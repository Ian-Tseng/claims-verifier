# Evaluation data

The public dataset contains [300 evaluation tasks and gold answers](e6_evaluation_v1/README.md): 100 mathematics, 100 programming and 100 finite-set logic tasks. These are previously inspected development instances.

No training records, method-specific prompts, reference maps or executor are distributed in the current tree. Read the dataset card for task definitions and the limits on comparing new tests with the [reported E6 results](../results/README.md).

## What is included?

The current dataset contains task descriptions, structured task inputs and gold answers only. It does not include training examples, model-specific prompts, intermediate representation targets or implementation code.

## What would a training example look like?

The following is a conceptual placeholder, not an actual training record or an executable format:

```text
Input: [task description and inputs]
Training target: [private structured representation] + [gold answer]
```

This illustrates the high-level use of structured supervision. The actual prompts, representation schema, operators, intermediate steps and target serialization are not included. The public task/gold records are evaluation material, not the representation-training examples used for the reported experiment.
