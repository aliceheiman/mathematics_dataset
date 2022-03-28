import re
import random
import itertools


def parse_synonyms(template):
    """Parses and returns a list of string templates.

    Args:
        template (string): a template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

    """

    def combine(current_selection, synonym_list, combinations=[]):
        """_summary_

        Args:
            current_selection (array): array of picked synonyms.
            synonym_list (array): synonyms to be picked

        Returns:
            _type_: _description_
        """

        # Make a copy
        selection = current_selection.copy()
        s_list = synonym_list.copy()

        # Base cases
        if len(s_list) == 0:
            return selection

        # Store all combinations
        combinations = []

        # If choices left, pop of the first choice list
        choices = s_list[0]
        s_list = s_list[1:]

        # Go through every synonym in the choices list and keep on combining
        for choice in choices:
            # Add the selection
            selection.append(choice)

            # Add all the found combinations
            found_combinations = combine(selection, s_list)

            if found_combinations != []:
                combinations.append(found_combinations)
                print(found_combinations)

            # Remove the last item to construct more variations from the same stem
            selection = selection[:-1]

        # Return all found combinations
        return combinations

    templates = []

    if "[" in template and "]" in template:

        # Get all synonyms enclosed in [] and convert into lists
        matches = re.findall("\[.*?\]", template)
        synonyms = [m[1:-1].split(", ") for m in matches]

        # Create every possible combination from the words
        combinations = combine([], synonyms)
        print("Combinations!")
        print(combinations)

    else:
        templates.append(template)

    return templates


template = "[Compute, Calculate] [5, five] times [7, seven]."
# parse_synonyms(template)

matches = re.findall("\[.*?\]", template)
synonyms = [m[1:-1].split(", ") for m in matches]

combinations = list(itertools.product(*synonyms))

print(combinations)
