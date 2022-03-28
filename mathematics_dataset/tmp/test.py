import re
import random
import itertools
from pprint import pprint


def translate(text, context=False):
    """Translates original text into specified language."""

    if context != False:
        text = text + context

    # Default to text if not found in translation
    return text


def parse_synonyms(template):
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


def parse(templates):
    """Parses and returns a list of string templates.

    Args:
        templates (array): a list of template strings. Converts "[Synonym1, Synonym2] ..." into separate list items.

    """

    # Store all templates
    all_templates = []

    # Go through all provided templates
    for template in templates:

        # Translate template
        translation = translate(template)

        # Parse synonyms
        translations = parse_synonyms(translation)

        # Add to all templates
        all_templates += translations

    # Return
    return all_templates


templates = [
    "[Let, Suppose, Given] {equality}. [Calculate, Compute] {variable}.",
    "What is {variable} in {equality}?",
    "Solve {equality} for {variable}.",
    "Find {variable} such that {equality}.",
    "Find {variable}, given that {equality}.",
    "Determine {variable} so that {equality}.",
    "Determine {variable}, given that {equality}.",
    "Solve {equality}.",
]

pprint(parse(templates))
