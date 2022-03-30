# Multilingual Mathematics Dataset

This dataset code generates mathematical question and answer pairs in different languages, from a range
of question types at roughly school-level difficulty. This is designed to test
the mathematical learning and algebraic reasoning skills of learning models in various languages.

Original paper: [Analysing Mathematical
Reasoning Abilities of Neural Models](https://openreview.net/pdf?id=H1gR5iR5FX)
(Saxton, Grefenstette, Hill, Kohli).

## Example questions

```
Question: Solve -42*r + 27*c = -1167 and 130*r + 4*c = 372 for r.
Answer: 4

Question: Calculate -841880142.544 + 411127.
Answer: -841469015.544

Question: Let x(g) = 9*g + 1. Let q(c) = 2*c + 1. Let f(i) = 3*i - 39. Let w(j) = q(x(j)). Calculate f(w(a)).
Answer: 54*a - 30

Question: Let e(l) = l - 6. Is 2 a factor of both e(9) and 2?
Answer: False

Question: Let u(n) = -n**3 - n**2. Let e(c) = -2*c**3 + c. Let l(j) = -118*e(j) + 54*u(j). What is the derivative of l(a)?
Answer: 546*a**2 - 108*a - 118

Question: Three letters picked without replacement from qqqkkklkqkkk. Give prob of sequence qql.
Answer: 1/110
```

## Pre-generated data

[Pre-generated files](https://console.cloud.google.com/storage/browser/mathematics-dataset)

### Version 1.2

Added more translation variations and synonym capabilities. Specify synonyms with brackets: \[Synonym 1, Synonym 2, Synonym 3, etc. \].

### Version 1.1

This is the updated multilingual version. New languages are added in the **lang** folder. The *lang* object translates all strings in the code specified by the language in the *generate_settings.py* file.

### Version 1.0

This is the version released with the original paper. It contains 2 million
(question, answer) pairs per module, with questions limited to 160 characters in
length, and answers to 30 characters in length. Note the training data for each
question type is split into "train-easy", "train-medium", and "train-hard". This
allows training models via a curriculum. The data can also be mixed together
uniformly from these training datasets to obtain the results reported in the
paper. Categories:

* **algebra** (linear equations, polynomial roots, sequences)
* **arithmetic** (pairwise operations and mixed expressions, surds)
* **calculus** (differentiation)
* **comparison** (closest numbers, pairwise comparisons, sorting)
* **measurement** (conversion, working with time)
* **numbers** (base conversion, remainders, common divisors and multiples,
  primality, place value, rounding numbers)
* **polynomials** (addition, simplification, composition, evaluating, expansion)
* **probability** (sampling without replacement)

## Getting the source

### PyPI

The easiest way to get the source is to use pip:

```shell
$ pip install mathematics_dataset
```

### From GitHub

Alternately you can get the source by cloning the mathematics_dataset
repository:

```shell
$ git clone https://github.com/deepmind/mathematics_dataset
$ pip install --upgrade mathematics_dataset/
```

## Generating examples

Generated examples can be printed to stdout via the `generate` script. For
example:

```shell
python -m mathematics_dataset.generate --filter=linear_1d
```

will generate example (question, answer) pairs for solving linear equations in
one variable.

Below is a list of available filters:
* linear_1d_composed
* linear_1d
* linear_2d_composed
* linear_2d
* polynomial_roots_composed
* polynomial_roots
* sequence_next_term
* sequence_nth_term
* add_or_sub_in_base
* add_or_sub
* add_sub_multiple
* div
* mixed
* mul_div_multiple
* mul
* nearest_integer_root
* simplify_surd
* differentiate_composed
* differentiate
* closest_composed
* closest
* kth_biggest_composed
* kth_biggest
* pair_composed
* pair
* sort_composed
* sort
* conversion
* time
* base_conversion
* div_remainder_composed
* div_remainder
* gcd_composed
* gcd
* is_factor_composed
* is_factor
* is_prime_composed
* is_prime

We've also included `generate_to_file.py` as an example of how to write the
generated examples to text files. You can use this directly, or adapt it for
your generation and training needs. To generate a range of questions into a directory, use:

```shell
python -m mathematics_dataset.generate_to_file --output_dir=directory_name
```

Note, make sure the directory does not already exist before qenerating questions to file.

## Adding More Languages

Copy the *template.txt* file in the **lang** folder and rename it to **lang.txt** with the two-character abbreviation for your language. To change the output language, change the **lang=** in the *generate_settings.py* file to the language abbreviation.

Synonyms are enclosed in square brackets (\[\]). The program will automatically create all combinations possible from the provided synonyms. This is a quick way to get more variations in the problem formulations. Multiple blocks of synonyms can be included in the same template. The program parses this template and produces a list of all variations. For example:

```
[Calculate, Determine] 5 [times, multiplied with] 7. 
```

Turns into:

```
Calculate 5 times 7.
Calculate 5 multiplied with 7.
Determine 5 times 7.
Determine 5 multiplied with 7.
```

## Dataset Metadata
The following table is necessary for this dataset to be indexed by search
engines such as <a href="https://g.co/datasetsearch">Google Dataset Search</a>.
<div itemscope itemtype="http://schema.org/Dataset">
<table>
  <tr>
    <th>property</th>
    <th>value</th>
  </tr>
  <tr>
    <td>name</td>
    <td><code itemprop="name">Mathematics Dataset</code></td>
  </tr>
  <tr>
    <td>url</td>
    <td><code itemprop="url">https://github.com/deepmind/mathematics_dataset</code></td>
  </tr>
  <tr>
    <td>sameAs</td>
    <td><code itemprop="sameAs">https://github.com/deepmind/mathematics_dataset</code></td>
  </tr>
  <tr>
    <td>description</td>
    <td><code itemprop="description">This dataset consists of mathematical question and answer pairs, from a range
of question types at roughly school-level difficulty. This is designed to test
the mathematical learning and algebraic reasoning skills of learning models.\n
\n
## Example questions\n
\n
```\n
Question: Solve -42*r + 27*c = -1167 and 130*r + 4*c = 372 for r.\n
Answer: 4\n
\n
Question: Calculate -841880142.544 + 411127.\n
Answer: -841469015.544\n
\n
Question: Let x(g) = 9*g + 1. Let q(c) = 2*c + 1. Let f(i) = 3*i - 39. Let w(j) = q(x(j)). Calculate f(w(a)).\n
Answer: 54*a - 30\n
```\n
\n
It contains 2 million
(question, answer) pairs per module, with questions limited to 160 characters in
length, and answers to 30 characters in length. Note the training data for each
question type is split into "train-easy", "train-medium", and "train-hard". This
allows training models via a curriculum. The data can also be mixed together
uniformly from these training datasets to obtain the results reported in the
paper. Categories:\n
\n
* **algebra** (linear equations, polynomial roots, sequences)\n
* **arithmetic** (pairwise operations and mixed expressions, surds)\n
* **calculus** (differentiation)\n
* **comparison** (closest numbers, pairwise comparisons, sorting)\n
* **measurement** (conversion, working with time)\n
* **numbers** (base conversion, remainders, common divisors and multiples,\n
  primality, place value, rounding numbers)\n
* **polynomials** (addition, simplification, composition, evaluating, expansion)\n
* **probability** (sampling without replacement)</code></td>
  </tr>
  <tr>
    <td>provider</td>
    <td>
      <div itemscope itemtype="http://schema.org/Organization" itemprop="provider">
        <table>
          <tr>
            <th>property</th>
            <th>value</th>
          </tr>
          <tr>
            <td>name</td>
            <td><code itemprop="name">DeepMind</code></td>
          </tr>
          <tr>
            <td>sameAs</td>
            <td><code itemprop="sameAs">https://en.wikipedia.org/wiki/DeepMind</code></td>
          </tr>
        </table>
      </div>
    </td>
  </tr>
  <tr>
    <td>citation</td>
    <td><code itemprop="citation">https://identifiers.org/arxiv:1904.01557</code></td>
  </tr>
</table>
</div>
