# Copyright 2018 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of how to write generated questions to text files.

Given an output directory, this will create the following subdirectories:

*   train-easy
*   train-medium
*   train-hard
*   interpolate
*   extrapolate

and populate each of these directories with a text file for each of the module,
where the text file contains lines alternating between the question and the
answer.

Passing --train_split=False will create a single output directory 'train' for
training data.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import random
import json

# Dependency imports
from mathematics_dataset.util import lang
from absl import app
from absl import flags
from absl import logging
from mathematics_dataset import generate_settings
from mathematics_dataset import generate
import six
from six.moves import range

FLAGS = flags.FLAGS

flags.DEFINE_boolean("train_split", True, "Whether to split training data by difficulty")
flags.DEFINE_boolean("reset_file", True, "Whether to reset the generated_data.json contents.")


def main(unused_argv):

    REPEAT = 1
    ANSWER_TEMPLATES = lang.l.parse(
        [
            "Answer:",
            "The answer is:",
            "The correct answer is:",
            "The answer is",
            "The correct answer is",
        ]
        + [""]
    )

    print(ANSWER_TEMPLATES)

    generate.init_modules(FLAGS.train_split)

    path = os.path.join("generated_data", "generated_data.json")

    # Reset file
    if FLAGS.reset_file:
        with open(path, "w") as text_file:
            pass

    logging.info("Writing to %s", path)

    for regime, flat_modules in six.iteritems(generate.filtered_modules):

        per_module = generate.counts[regime]
        for module_name, module in six.iteritems(flat_modules):
            with open(path, "a") as text_file:
                for _ in range(REPEAT):
                    for _ in range(per_module):
                        problem, _ = generate.sample_from_module(module)

                        answer_template = random.choice(ANSWER_TEMPLATES)
                        answer_template = "" if answer_template == "" else answer_template + " "

                        text_sample = str(problem.question) + "\n"
                        text_sample += answer_template + str(problem.answer) + "\n"
                        text_sample += "\n"

                        text_file.write(json.dumps({"text": text_sample}, ensure_ascii=False))
                        text_file.write("\n")

            logging.info("Written %s", path)


if __name__ == "__main__":
    app.run(main)
