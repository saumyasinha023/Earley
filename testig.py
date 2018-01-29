
def test():
    array = []
    with open("Random", 'r') as f:
        ans = f.read().splitlines()
        pattern_line = ""
        flag = 0
        for each in ans:
            each.strip()
            if "#" in each:
                continue
            if pattern_line and pattern_line[-1] == ";":
                array.append(pattern_line)
                pattern_line = ""
            if each and each[-1] == ";":
                pattern_line = pattern_line + each
                array.append(pattern_line)
                pattern_line = ""
            elif ":" in each:
                if pattern_line:
                    array.append(pattern_line)
                pattern_line = ""
                pattern_line = each
            else:
                pattern_line += each
        if pattern_line:
            array.append(pattern_line)
    for each in array:
        print(each)
test()