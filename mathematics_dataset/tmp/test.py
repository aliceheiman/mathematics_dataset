import re
import random
import itertools


def parse_synonyms(template):
    """Parses and returns a list of string templates.

    Args:
        template (string): a template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

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


template = "[Compute, Calculate] [5, five] times [7, seven]."
print(parse_synonyms(template))
