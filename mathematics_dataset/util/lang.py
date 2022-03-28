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

"""Functionality for translating mathematics questions."""

import os
import sys
import re
import itertools


class Lang:
    def __init__(self, language):
        self.lang = language
        self.lookup = {}
        self.load_lookup()

    def load_lookup(self):
        # Get translation file
        filename = os.path.join("mathematics_dataset", "lang", f"{self.lang}.txt")

        # Check if translation file exists
        if not os.path.isfile(filename):
            exit(f"No translation file found for lang={self.lang}. Please add {self.lang}.txt in the /lang folder.")

        # Load contents into default dict
        with open(filename, "r") as f:
            contents = f.read()

        for line in contents.split("\n"):
            if line == "" or line.startswith("#"):
                continue

            # Get context
            context = ""

            if line.startswith("!"):
                components = line.split("!")
                context = components[1]
                line = components[2][1:]

            try:
                original, translation = line.split(" ### ")[:2]
                original = original.lstrip()
                translation = translation.rstrip()

                self.lookup[original + context] = translation
            except:
                continue

    def translate(self, text, context=False):
        """Translates original text into specified language."""

        if context != False:
            text = text + context

        # Default to text if not found in translation
        if text not in self.lookup:
            print(f"!! {text} not in translation file!")
            return text
        else:
            return self.lookup[text]

    def parse_synonyms(self, template):
        """Parses and returns a list of string templates.

        Args:
            template (string): a template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

        Returns:
            templates (array): a list of generated template strings from the original.

        """

        templates = []

        if "[" in template and "]" in template:

            # Get all synonyms enclosed in [] and convert into lists
            matches = re.findall("\[.*?\]", template)
            synonyms = [m[1:-1].split(", ") for m in matches]

            # Create every possible combination from the words
            combinations = list(itertools.product(*synonyms))

            # Substitute every match with the correct synonym
            for combination in combinations:

                # Make a new template
                new_template = template

                # Replace the synonym match block with every word combination
                for match_block, word in zip(matches, combination):
                    new_template = new_template.replace(match_block, word)

                # Add new template to templates
                templates.append(new_template)

        else:
            # No synonyms, just return the original template
            templates.append(template)

        return templates

    def parse(self, templates):
        """Parses and returns a list of string templates.

        Args:
            templates (array): a list of template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

        """

        # Store all templates
        all_templates = []

        # Go through all provided templates
        for template in templates:

            # Translate template
            translation = self.translate(template)

            # Parse synonyms
            translations = self.parse_synonyms(translation)

            # Add to all templates
            all_templates += translations

        # Return
        return all_templates


def init_translation(language="en"):
    # Create Lang object
    global l
    l = Lang(language=language)
