with open('phrase', 'r') as f:
    phrases = f.readlines()
    phrases = list(map(lambda x: x[:-1], phrases))
    phrases = list(filter(lambda x: len(x) > 2, phrases))

marked = []

for phrase in phrases:  # type: str
    if phrase in marked:
        continue
    if phrase[::-1] == phrase:
        continue
    if phrase[::-1] in phrases:
        print(phrase, phrase[::-1])
        marked.append(phrase[::-1])
