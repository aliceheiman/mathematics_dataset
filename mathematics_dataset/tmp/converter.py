""" 
Converts a portion of language translations in the format ENGLISH ### LANGUAGE into 
lang.l.translate("text") statements that can be copied into the program.
"""

import pyperclip

print("Reading from clipboard...")
contents = pyperclip.paste()
contents = contents.split("\n")

statements = []

for line in contents:
    if line == "":
        continue

    eng, lang = line.split(" ### ")
    statements.append(f'lang.l.translate("{eng}"),')

statements = "\n".join(statements)

pyperclip.copy(statements)
print("Language statements copied to clipboard.")
