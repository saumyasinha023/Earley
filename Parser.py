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
        toAppend = [RHS + " -> " + " * " + each, state_number, state_number]
        if toAppend not in s[state_number]:
            enqueue(state_number, toAppend)


def scanner(row_elem,i):
    for element in s[i]:
        fetched = extractAfterStarState(element[0])
        if dict["W"][i] in dict[fetched]:
            toAppend = [fetched + " -> " + dict["W"][i] + " * ", row_elem[2], row_elem[2]+1]
            enqueue(row_elem[2] + 1, toAppend)


def completer(row_elem, i):
    print(row_elem,"VARDAN")
    LHS = find_LHS(row_elem[0])
    for each in s[row_elem[1]]:
        if ("*" + " " + LHS) in each[0]:
            left = each[0].split('*')[0]
            right = each[0].split('*')[1]
            mid = right.split(" ")[1]
            toAppend = [left + mid + " * " + "".join(right.split()[2:]),row_elem[1],row_elem[2]]
            enqueue(row_elem[1] + 1, toAppend)

def find_LHS(string):
    emails = re.findall(r'(?:^|(?:[->?!]\s))([a-zA-Z]+)', string[0])
    if emails:
        final = emails[0].strip()
        return (final)
    else:
        print(string[0])


def Earley_parser(words):
    global s
    global current_pos
    enqueue(0, ["Z → * S", 0, 0])
    for i in range(len(words) + 1):
        for row_elem in s[i]:
            RHS = extractAfterStarState(row_elem[0])
            # if RHS==0 and RHS not in dict:
            #     continue
            # if s[i].index(row_elem) == 0 and RHS == 0:
            #     continue
            if RHS != 0 and RHS not in pos:
                predictor(i, RHS)
            elif RHS != 0 and RHS in pos:
                scanner(row_elem,i)
            else:
                completer(row_elem, i)


def enqueue(state, chart_entry):
    global s
    i = 0
    for iter in s[state]:
        if iter[0] == chart_entry[0]:
            i = 1
    if i == 0:
        s[state].append(chart_entry)


def checkNextState(string, state):
    pass


def initialize(words):
    global s
    s = [[] for i in range(len(words) + 1)]
    Earley_parser(dict["W"])


initialize(dict["W"])
# for each in s:
#     for elem in each:
#         print(elem)
