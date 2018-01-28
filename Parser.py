import re
import atexit
import sys
import fileinput
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict

ps = PorterStemmer()

#
# @atexit.register
# def quit_gracefully():
#     print("ENDFILE")


def findType(inputToken):
    if (re.match('^[-+]?[0-9]+$', inputToken)):
        return "INT"
    elif (re.match('[+-]?([0-9]*[.])?[0-9]+', inputToken)):
        return "DOUBLE"
    elif (re.match('\W', inputToken)):
        return "OP"
    elif (type('\w') is str):
        return "STRING"
    # else:

    #     @atexit.register
    #     def quit_gracefully():
    #         print("ENDFILE")
    #         sys.exit(0)


count = 0
grammar = defaultdict(list)
partofspeech = set()

for line in fileinput.input():
    # sys.exit("ENDFILE")
    s = re.search('[^(a-zA-Z|\*|\s|\:|\=|\;|\-|\||\#|\.|\?|\!|\,|\'|\")]', line)
    if s is not None and s.group(0) is not None:
        exit("Erroneous input")
    elif line.isspace():
        continue
    else:
        if count==0:
            print("Stemmer: ")
            count += 1

    for each in line.split(';'):
        each = each.lstrip()

        if re.search('^([a-zA-Z\-]+)\s*[\:|\=]\s*([a-zA-Z\-\|\*\s*]*)', each) is not None:
            parts = re.search('([a-zA-Z\-]+)\s*[\:|\=]\s*([a-zA-Z\-\|\*\s*\'\,\.\?\!]*)', each)
            LHS = parts.group(1)
            if parts.group(2).find('|') == -1 and LHS == 'W':
                subpart = re.split('\s+', parts.group(2))
            else:
                subpart = re.split('\s*\|\s*', parts.group(2))
        elif re.search('\s*\|\s*[a-zA-Z\-\s]+', each) is not None:
            childpart = re.findall('\s*\|\s*([a-zA-Z\-\s]+)', each)
            for x in childpart:
                childsubpart = x
                grammar[LHS].append(childsubpart.rstrip())
        elif re.search('\#\s*[a-zA-Z]+', each) is not None:
            continue

        for i in range(len(subpart)):
            if subpart[i].islower():
                if LHS != 'W':
                    partofspeech.add(LHS)
            if LHS == 'W' and subpart[i] is not '':
                a = re.search('[a-zA-Z\-]+', subpart[i])
                b = a.group(0)
                RHS = ps.stem(b)
            else:
                RHS = subpart[i]
            grammar[LHS].append(RHS.rstrip())

        for w in word_tokenize(each):
            type_of_word = findType(w)
            if line.find('=') == -1:
                if re.search('\|*\s*([a-zA-Z\-\s]+)', w) is not None:
                    stem_parts = re.split('\|', w)
                    for i in range(len(stem_parts)):
                        type_of_word = findType(stem_parts[i])
                        print(stem_parts[i], ' ', type_of_word, ' ', fileinput.lineno())
                else:
                    print(w, ' ', type_of_word, ' ', fileinput.lineno())

            else:
                if re.search('[A-Za-z]', w) is not None and w != "W":
                    print(w, ' ', type_of_word, ' ', fileinput.lineno(), ' ', ps.stem(w), ' ')
                else:
                    print(w, ' ', type_of_word, ' ', fileinput.lineno())

print("ENDFILE")
print("-----GRAMMAR------")
for x in grammar:
    print(x, ' : ', grammar[x])
print('partofspeech: ', partofspeech)

def extractAfterStarState(string):
    emails = re.search(r'\^\s*(.*)\b', string)
    if emails:
        final = emails.group(1).split()[0]
        return (final)
    else:
        return 0


def predictor(row_elem):
    RHS = extractAfterStarState(row_elem[0])
    LHS = find_LHS(row_elem[0])
    if LHS not in partofspeech:
        for each in grammar[RHS]:
            toAppend = [RHS + " -> " + " ^ " + each, row_elem[2], row_elem[2], "predictor"]
            if toAppend not in s[row_elem[2]]:
                enqueue(row_elem[2], toAppend)


def scanner(row_elem, i):
    fetched = extractAfterStarState(row_elem[0])
    if i < len(grammar["W"]) and grammar["W"][i] in grammar[fetched]:
        toAppend = [fetched + " -> " + grammar["W"][i] + " ^ ", row_elem[2], row_elem[2] + 1, "scanner"]
        enqueue(row_elem[2] + 1, toAppend)


def completer(row_elem):
    LHS = find_LHS(row_elem[0])
    for each in s[row_elem[1]]:
        if ("^" + " " + LHS) in each[0] and LHS != "S":
            left = each[0].split('^')[0]
            right = each[0].split('^')[1]
            mid = right.split(" ")[1]
            toAppend = [left + mid + " ^ " + " ".join(right.split()[1:]), each[1], row_elem[2], "completer"]
            enqueue(row_elem[2], toAppend)


def find_LHS(string):
    emails = re.findall(r'(?:^|(?:[->?!]\s))([a-zA-Z]+)', string)
    if emails:
        final = emails[0].strip()
        return (final)
    else:
        print(string[0])


def Earley_parser(words):
    global s
    global current_pos
    enqueue(0, ["Z -> ^ S", 0, 0])
    for i in range(len(words) + 1):
        for row_elem in s[i]:
            RHS = extractAfterStarState(row_elem[0])
            if RHS != 0 and RHS not in partofspeech:
                predictor(row_elem)
            elif RHS != 0 and RHS in partofspeech:
                scanner(row_elem, i)
            else:
                completer(row_elem)


def enqueue(state, chart_entry):
    global s
    i = 0
    for iter in s[state]:
        if iter[0] == chart_entry[0]:
            i = 1
    if i == 0:
        s[state].append(chart_entry)


def initialize(words):
    global s
    s = [[] for i in range(len(words) + 1)]
    Earley_parser(grammar["W"])


initialize(grammar["W"])
for each in s:
    for elem in each:
        print(elem)
