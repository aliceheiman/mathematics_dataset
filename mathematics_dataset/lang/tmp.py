import os

# STRINGS TO TEMPLATE
""" filename = os.path.join('mathematics_dataset', 'lang', 'strings.txt')

with open(filename) as f:
    contents = f.read()

lines = contents.split('\n')
template = []
for line in lines:
    if line == '' or line.startswith('#'):
        template.append(line)
    else:
        template.append(line + ' ### ')

template = '\n'.join(template)

filename = os.path.join('mathematics_dataset', 'lang', 'template.txt')
with open(filename, 'w') as f:
    f.write(template) """

# POPULATE STRINGS TEMPLATE
def populate_strings_template():
    # filename = os.path.join("mathematics_dataset", "lang", "sv.txt")
    filename = os.path.join("sv.txt")

    with open(filename) as f:
        contents = f.read()

    lines = contents.split("\n")
    template = []
    for line in lines:
        if line == "" or line.startswith("#"):
            template.append(line)
        else:
            string = line.split(" ### ")[0]
            template.append(string)

    template = "\n".join(template)
    # filename = os.path.join("mathematics_dataset", "lang", "_strings.txt")
    filename = os.path.join("_strings.txt")
    with open(filename, "w") as f:
        f.write(template)


# POPULATE ENGLISH TEMPLATE
def populate_english_template():
    # filename = os.path.join("mathematics_dataset", "lang", "_strings.txt")
    filename = os.path.join("_strings.txt")

    with open(filename) as f:
        contents = f.read()

    lines = contents.split("\n")
    template = []
    for line in lines:
        if line == "" or line.startswith("#"):
            template.append(line)
        else:
            template.append(line + " ### " + line)

    template = "\n".join(template)

    # filename = os.path.join("mathematics_dataset", "lang", "en.txt")
    filename = os.path.join("en.txt")
    with open(filename, "w") as f:
        f.write(template)


# POPULATE TEMPLATE FILE
def populate_template_file():
    # filename = os.path.join("mathematics_dataset", "lang", "_strings.txt")
    filename = os.path.join("_strings.txt")

    with open(filename) as f:
        contents = f.read()

    lines = contents.split("\n")
    template = []
    for line in lines:
        if line == "" or line.startswith("#"):
            template.append(line)
        else:
            splitter = ["_" if not t.startswith("{") else t for t in line.split(" ")]
            temp_line = []
            prev_t = ""
            for t in splitter:
                if t == prev_t:
                    prev_t = t
                    continue

                prev_t = t
                temp_line.append(t)

            temp_line = " ".join(temp_line)

            template.append(line + " ### " + temp_line)

    template = "\n".join(template)

    # filename = os.path.join("mathematics_dataset", "lang", "template.txt")
    filename = os.path.join("_template.txt")
    with open(filename, "w") as f:
        f.write(template)


## COUNT STRINGS
def count_strings():
    # filename = os.path.join("mathematics_dataset", "lang", "_strings.txt")
    filename = os.path.join("_strings.txt")

    with open(filename) as f:
        contents = f.read()

    lines = contents.split("\n")
    count = 0

    for line in lines:
        if line == "" or line.startswith("#"):
            continue

        count += 1

    print(f"Strings to translate: {count}")
