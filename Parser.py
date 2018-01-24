import re

pos = ["Verb", "Aux", "Det", "Proper-Noun", "Pronoun", "Noun"]
incomplete = ["S", "NP", "VP", "PP"]
dict = {"S": ["NP VP", "Aux NP VP", "VP"],
        "NP": ["Pronoun", "Proper-Noun", "Det Nominal"],
        "VP": ["Verb", "Verb NP", "Verb NP PP", "Verb PP", "VP PP"],
        "Aux": ["can", "will"],
        "Det": ["the", "that"],
        "Pronoun": ["he", "she"],
        "Proper-Noun": ["mary", "john"],
        "Nominal": ["Noun", "Nominal Noun", "Nominal PP"],
        "Noun": ["book", "flight"],
        "Verb": ["do", "work", "book"],
        "PP": ["Prep" " NP"],
        "Prep": ["in", "on", "at"],
        "W": ["book", "that", "flight"]
        }


def extractAfterStarState(string):
    emails = re.search(r'\*\s*(.*)\b', string)
    if emails:
        final = emails.group(1).split()[0]
        return (final)
    else:
        return 0


def predictor(state_number, RHS):
    for each in dict[RHS]:
        toAppend = RHS + "->" + " * " + each
        if toAppend not in s[state_number]:
            enqueue(state_number, toAppend)


def scanner(i):
    for element in s[i]:
        fetched = extractAfterStarState(element)
        if dict["W"][i] in dict[fetched]:
            toAppend = fetched + "->" + dict["W"][i] + " * " + "["+
            print(toAppend)
            enqueue(i + 1, toAppend)


def completer(row_elem, i):
    LHS = find_LHS(row_elem)
    pass


def find_LHS(string):
    emails = re.findall(r'(?:^|(?:[->?!]\s))([a-zA-Z]+)', string)
    if emails:
        final = emails[0].strip()
        return (final)


def Earley_parser(words):
    global s
    global current_pos
    enqueue(0,0, "γ → * S")
    for i in range(len(words) + 1):
        for row_elem in s[i]:
            RHS = extractAfterStarState(row_elem)
            # if s[i].index(row_elem) == 0 and RHS == 0:
            #     continue
            if RHS != 0 and RHS not in pos:
                predictor(i, RHS)
            elif RHS != 0 and RHS in pos:
                scanner(i)
            else:

                completer(row_elem, i)


def enqueue(state, chart_entry):
    global s
    if state not in s[state]:
        s[state].append(chart_entry)


def checkNextState(string, state):
    pass


def initialize(words):
    global s
    s = [[] for i in range(len(words) + 1)]
    Earley_parser(dict["W"])


initialize(dict["W"])
for each in s:
    for elem in each:
        print(elem)
