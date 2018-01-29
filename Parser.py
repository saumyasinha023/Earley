import re
import sys
import fileinput
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict


class earleyParser():

    def __init__(self):
        self.ps = PorterStemmer()
        self.partOfSpeech = set()
        self.grammar = defaultdict(list)
        self.stemmer_array = []

    def findDataType(self, inputToken):
        # method created to determine the data-type of the
        # input value being stemmed and classifying them in
        # int, double,op and string

        if (re.match('^[-+]?[0-9]+$', inputToken)):
            return "INT"
        elif (re.match('[+-]?([0-9]*[.])?[0-9]+', inputToken)):
            return "DOUBLE"
        elif (re.match('\W', inputToken)):
            return "OP"
        elif (type('\w') is str):
            return "STRING"

    def preProcess(self):
        # method to pre process the grammar from input
        # before applying stemmer to it. This method also
        # determines if any input is incorrect.
        count = 0
        # global grammar
        # implementation of stemmer

        cTemp = sTemp = colon = semi = 0
        eachLine = ""
        finalInput = []
        self.stemmer_array = []
        for line in fileinput.input():
            for eachWord in word_tokenize(line):
                if count == 0:
                    # print("Stemmer:")
                    self.stemmer_array.append("".join(["\nStemmer: "]))
                    count += 1
                wordDataType = self.findDataType(eachWord)
                if line.find('=') == -1:
                    if re.search('\|*\s*([a-zA-Z\-\s]+)', eachWord) is not None:
                        stemmedPart = re.split('\|', eachWord)
                        for i in range(len(stemmedPart)):
                            if len(stemmedPart) > 1 and i == 1 and stemmedPart[i] is not '':
                                self.stemmer_array.append("".join(['|', ' ', 'OP', ' ', str(fileinput.lineno())]))
                            if stemmedPart[i] is '':
                                self.stemmer_array.append("".join(['|', ' ', 'OP', ' ', str(fileinput.lineno())]))
                            else:
                                wordDataType = self.findDataType(stemmedPart[i])
                                self.stemmer_array.append(
                                    "".join([stemmedPart[i], ' ', wordDataType, ' ', str(fileinput.lineno())]))
                    else:
                        self.stemmer_array.append("".join([eachWord, ' ', wordDataType, ' ', str(fileinput.lineno())]))
                else:
                    if re.search('[A-Za-z]', eachWord) is not None and eachWord != "W":
                        self.stemmer_array.append(
                            "".join([eachWord, ' ', wordDataType, ' ', str(fileinput.lineno()), ' ',
                                     self.ps.stem(eachWord).lower(), ' ']))
                    else:
                        self.stemmer_array.append("".join([eachWord, ' ', wordDataType, ' ', str(fileinput.lineno())]))

            line.strip()
            if "#" in line:
                continue
            if eachLine and eachLine[-1] == ";":
                finalInput.append(eachLine)
                eachLine = ""
            if line and line[-1] == ";":
                eachLine = eachLine + line
                finalInput.append(eachLine)
                eachLine = ""
            elif ":" in line:
                if eachLine:
                    finalInput.append(eachLine)
                eachLine = ""
                eachLine = line
            else:
                eachLine += line
        if eachLine:
            finalInput.append(eachLine)
        for line in finalInput:
            s = re.search('[^(a-zA-Z|\*|\s|\:|\=|\;|\-|\||\#|\.|\?|\!|\,|\'|\")]', line)
            if s is not None and s.group(0) is not None:
                print("Error in input. Illegal elements in input!")
                exit("Error in input. Illegal elements in input!")
            elif line.isspace():
                continue

            semi = sTemp + line.count(';')
            colon = cTemp + line.count(':')
            if semi == colon:
                semi = colon = sTemp = cTemp = 0
            elif semi > colon:
                print("Error in input. Incorrect semicolons!")
                sys.exit("Error in input. Incorrect semicolons!")
            else:
                cTemp = colon
                sTemp = semi

            for each in line.split(';'):
                each = each.lstrip()
                if re.search('^([a-zA-Z\-]+)\s*[\:|\=]+\s*([a-zA-Z\-\|\*\s*\'\"\,\.\?\!]*)', each) is not None:
                    parts = re.search('^([a-zA-Z\-]+)\s*[\:|\=]+\s*([a-zA-Z\-\|\*\s*\'\"\,\.\?\!]*)', each)
                    leftSideVal = parts.group(1)
                    if parts.group(2).find('|') == -1 and leftSideVal == 'W':
                        subString = re.split('\s+', parts.group(2))
                    else:
                        subString = re.split('\s*\|\s*', parts.group(2))
                elif re.search('\s*\|\s*[a-zA-Z\-\s]+', each) is not None:
                    childSubString = re.findall('\s*\|\s*([a-zA-Z\-\s]+)', each)
                    for x in childSubString:
                        childSubPart = x
                        childSubPart = re.sub('[\n\t\r]+', ' ', childSubPart)
                        self.grammar[leftSideVal].append(childSubPart.rstrip())
                elif re.search('\#\s*[a-zA-Z]+', each) is not None:
                    continue

                for i in range(len(subString)):
                    if subString[i].islower():
                        if leftSideVal != 'W':
                            self.partOfSpeech.add(leftSideVal)
                    if leftSideVal == 'W':
                        a = re.search('[a-zA-Z\-]+', subString[i])
                        if subString[i] == '' or a == None:
                            continue
                        b = a.group(0)
                        rightSideVal = self.ps.stem(b)
                        rightSideVal = rightSideVal.lower()
                    else:
                        rightSideVal = subString[i]
                    rightSideVal = re.sub('[\n\t\r]+', ' ', rightSideVal)
                    self.grammar[leftSideVal].append(rightSideVal.rstrip())

        if semi < colon:
            print("Error in input. Missing semicolons!")
            sys.exit("Error in input. Missing semicolons!")
        # if "W" not in self.grammar:
        #     sys.exit("Error in input. Missing W!")
        if not self.grammar:
            print("Error. No Input!")
            sys.exit("Error. No Input!")
        self.stemmer_array.append("".join(["ENDFILE"]))

    def findValueAfterStarInRhs(self, string):
        # method to find out the value on the right
        # side of * element
        string = re.search(r'\^\s*(.*)\b', string)
        if string:
            out = string.group(1).split()[0]
            return (out)
        else:
            return 0

    def predictor(self, rowElement):
        # method to implement predictor function of Earley-Parser
        # which expands and parsers through all non-terminal
        # values available.
        RightSideValue = self.findValueAfterStarInRhs(rowElement[0])
        LeftSideValue = self.findLhs(rowElement[0])
        if LeftSideValue not in self.partOfSpeech:
            for each in self.grammar[RightSideValue]:
                eachRow = [RightSideValue + " -> " + " ^ " + each, rowElement[2], rowElement[2], "Predictor"]
                if eachRow not in s[rowElement[2]]:
                    self.enqueue(rowElement[2], eachRow)

    def scanner(self, rowElement, i):
        # method to implement scanner function of Earley-Parser
        # which finds if the available terminal element is
        # present in the grammar
        valAfterRhs = self.findValueAfterStarInRhs(rowElement[0])
        if i < len(self.grammar["W"]) and self.grammar["W"][i] in self.grammar[valAfterRhs]:
            eachRow = [valAfterRhs + " -> " + self.grammar["W"][i] + " ^ ", rowElement[2], rowElement[2] + 1, "Scanner"]
            self.enqueue(rowElement[2] + 1, eachRow)

    def completer(self, rowElement):
        # method to implement completer function of Earley-Parser
        # which increments the position ^ in the parsed grammar depending
        # upon the output of scanner
        LhsVal = self.findLhs(rowElement[0])
        for each in s[rowElement[1]]:
            if ("^" + " " + LhsVal) in each[0] and LhsVal != "S":
                left = each[0].split('^')[0]
                right = each[0].split('^')[1]
                mid = right.split(" ")[1]
                eachRow = [left + mid + " ^ " + " ".join(right.split()[1:]), each[1], rowElement[2], "Completer"]
                self.enqueue(rowElement[2], eachRow)

    def findLhs(self, string):
        # method to find the left hand side value of each row of
        # input
        leftSideVal = re.findall(r'(?:^|(?:[->?!]\s))([a-zA-Z]+)', string)
        if leftSideVal:
            final = leftSideVal[0].strip()
            return (final)
        else:
            print(string[0])

    def Earley_parser(self, words):
        # main method of Earley-Parser which calls the 3 functions:
        # predictor, scanner, completer depending upon the input
        global s
        self.enqueue(0, ["Z -> ^ S", 0, 0, "Dummy start state"])
        for i in range(len(words) + 1):
            for rowElement in s[i]:
                RHS = self.findValueAfterStarInRhs(rowElement[0])
                if RHS != 0 and RHS not in self.partOfSpeech:
                    self.predictor(rowElement)
                elif RHS != 0 and RHS in self.partOfSpeech:
                    self.scanner(rowElement, i)
                else:
                    self.completer(rowElement)

    def enqueue(self, state, chart_entry):
        # method to input the row element generated  from other methods,
        # into the queue
        global s
        i = 0
        for row in s[state]:
            if row[0] == chart_entry[0]:
                i = 1
        if i == 0:
            s[state].append(chart_entry)

    def createGrammar(self, words):
        # method to parse the given input and create a
        # dictionary to hold the values as key and values.
        global s
        s = [[] for i in range(len(words) + 1)]
        for word in self.grammar["W"]:
            found = 0
            for x in self.grammar:
                if x != "W":
                    for j in self.grammar[x]:
                        if j == word:
                            found += 1
            if found == 0:
                print("Error in input. Parsing could not be completed!")
                exit("Error in input. Parsing could not be completed!")
        self.Earley_parser(self.grammar["W"])

    def printStemmer(self):
        for each in self.stemmer_array:
            print(each)

    def printCharts(self):
        # method created to print the charts generated while parsing the grammar
        i = j = 0
        print("\nParsed Chart:")
        for each in s:
            print("\nChart[" + str(i) + "]\n")
            i += 1
            for elem in each:
                print("S" + str(j) + " " + elem[0], str([elem[1], elem[2]]), elem[-1])
                j += 1


E = earleyParser()
E.preProcess()
E.createGrammar(E.grammar["W"])
E.printStemmer()
E.printCharts()
