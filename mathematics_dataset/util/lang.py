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

        """

        def combine(current_selection, synonym_list):
            """_summary_

            Args:
                current_selection (array): array of picked synonyms.
                synonym_list (array): synonyms to be picked

            Returns:
                _type_: _description_
            """

            # Base cases
            if len(synonym_list) == 0:
                return current_selection

            # If choices left, pop of the first choice list
            choices = synonym_list[0]
            synonym_list = synonym_list[1:]

            # Go through every synonym in the choices list and keep on combining
            for choice in choices:
                current_selection.append(choice)
                combine(current_selection, synonym_list)

        templates = []

        if "[" in template and "]" in template:

            # Get all synonyms enclosed in [] and convert into lists
            matches = re.findall("\[.*?\]", template)
            synonyms = [m[1:-1].split(", ") for m in matches]

            # Create every possible combination from the words
            combinations = combine([], synonyms)

        else:
            templates.append(template)

        return templates

    def parse(self, templates):
        """Parses and returns a list of string templates.

        Args:
            templates (array): a list of template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

            Example template: Compute 5 times 5. ### Beräkna 5 gånger 5.
        """

        all_templates = []

        for template in templates:

            # Template
            if "[" in template and "]" in template:
                # Get synonyms enclosed in brackets from english and translation
                eng_synonyms, lang_synonyms = re.findall("\[.*?\]", template)

                # Go through each item in each block
                eng_block = eng_synonyms[1:-1].split(", ")
                lang_block = lang_synonyms[1:-1].split(", ")

                for eng_syn, lang_syn in zip(eng_block, lang_block):
                    new_template = template.replace(eng_block)


def init_translation(language="en"):
    # Create Lang object
    global l
    l = Lang(language=language)
