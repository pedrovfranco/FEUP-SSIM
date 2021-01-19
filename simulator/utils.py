def listToString(list):
    string = ''
    for element in list:
        string += element + ", "

    if string != "":
        string = string[:-2]

    return string

def AIDToString(list):
    string = ''
    for element in list:
        string += element.localname + ", "

    if string != "":
        string = string[:-2]

    return string