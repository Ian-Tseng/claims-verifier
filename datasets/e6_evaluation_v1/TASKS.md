# Task definitions

These definitions specify the problems in the evaluation file. They do not specify a model's reasoning method, prompt template or intermediate representation. Answers for mathematics and programming are strings; logic answers are objects containing an `answer` list of sorted integers.

## Mathematics

Inputs use `operands` for two-number tasks or `inputs` for named quantities.

| Task | Requested result |
|---|---|
| addition | a + b |
| multiplication, rectangle_area | a * b |
| exact_division | a / b; supplied cases divide exactly and b is nonzero |
| multiply_then_add | a * b + c |
| sum_then_multiply | (a + b) * c |
| difference_of_products | a * b - c * d |
| square_then_subtract | a * a - b |

## Programming

Return two lines of text, in the order listed. Lists retain order and repeated values unless the task explicitly removes duplicates.

| Task | First line; second line |
|---|---|
| sum_product | Sum of x and y; product of x and y |
| loop_sum_length | Sum of list values; list length |
| even_sum_count | Sum of even values; number of even values |
| positive_square_total | Sum of squares of positive values; number of positive values |
| reverse_uppercase_length | Reversed text converted to uppercase; text length |
| unique_preserve_order_join | First occurrence of each value joined with a vertical bar; number of distinct values |

## Finite-set logic

Read a, b and c from `sets` where present, otherwise directly from the input object. Complements are relative to the supplied universe U.

| Task | Requested set |
|---|---|
| or | Union of a and b |
| not | Elements of U outside a |
| union_then_intersection | Intersection of the union of a and b with c |
| difference_then_union | Union of a minus b with c |
| symmetric_difference_then_complement | Elements of U outside the symmetric difference of a and b |
| implication_then_intersection | Intersection of c with the union of U minus a and b |

Use the task inputs when evaluating a model. Keep the gold `answer` separate until scoring. These previously inspected development instances are not an untouched held-out test.
