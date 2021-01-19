def listToString(list):
    string = ''
    for element in list:
        string += element + ", "

    if string != "":
        string = string[:-2]

    return string

def AIDToString(aids):
    string = ''
    for element in aids:
        string += element.localname + ", "

    if string != "":
        string = string[:-2]

    return string

def daysOfMonth(m):
    months = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 21}

    return months.get(m)

def getWorkers(aids):
    workers = list()
    for elem in aids:
        workers.append(elem.localname)
    return workers

def unorderedListsComparison(list1, list2):
    temp1 = list1
    temp2 = list2
    temp1.sort()
    temp2.sort()
    return temp1 == temp2