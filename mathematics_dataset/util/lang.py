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
                original = original.strip()
                translation = translation.strip()

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


def init_translation(language="en"):
    # Create Lang object
    global l
    l = Lang(language=language)
