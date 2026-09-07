"""Standalone educational map execution; no trained model or private core."""
import json
from pathlib import Path


def evaluate_example(mapping):
    if mapping.get("operation") != "add":
        raise ValueError("This public illustration supports addition only")
    values = mapping["components"]
    left, right = values["left"], values["right"]
    if type(left) is not int or type(right) is not int:
        raise ValueError("Components must be integers")
    return left + right


if __name__ == "__main__":
    example = json.loads((Path(__file__).parent / "demo" / "example_map.json").read_text(encoding="utf-8"))
    answer = evaluate_example(example["map"])
    print(json.dumps({"mode": "educational illustration; no model inference", "question": example["question"], "map": example["map"], "computed_answer": answer, "expected_answer": example["expected_answer"], "matches_expected": answer == example["expected_answer"]}, indent=2))
