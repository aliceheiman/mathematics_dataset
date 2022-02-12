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

# POPULATE ENGLISH TEMPLATE
filename = os.path.join('mathematics_dataset', 'lang', '_strings.txt')

with open(filename) as f:
    contents = f.read()

lines = contents.split('\n')
template = []
for line in lines:
    if line == '' or line.startswith('#'):
        template.append(line)
    else:
        template.append(line + ' ### ' + line)

template = '\n'.join(template)

filename = os.path.join('mathematics_dataset', 'lang', 'en.txt')
with open(filename, 'w') as f:
    f.write(template)