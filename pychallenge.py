def contains(s1,s2):
    j = 0
    while (True):
        currChar = ""
        i = j
        for i in range(j,len(s2)):
            currChar += s2[i]
            if currChar == s1:
                return True
        j += 1
        if j == len(s2) - 1:
            return False
print(contains("mesa", "this is a test"))