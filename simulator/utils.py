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

def daysOfMonth(m, year):

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

    if year%4 == 0:
        months = {
        1: 31,
        2: 29,
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

def getRewardsNames(rewards):
    rewards_names = list()
    for reward in rewards:
        rewards_names.append(reward[0])
    return rewards_names

def getGpReward(rewards, reward_name):
    for reward in rewards:
        if reward[0] == reward_name:
            return reward[1]

def itemToString(item):
    return str(item[0]) + '/' + str(item[1])

def StringToitem(string):
    division = string.find('/')
    return [string[:division], string[division+1:]]

def epgpToString(ep, gp):
    return str(ep) + '/' + str(gp)

def StringToEpgp(string):
    division = string.find('/')
    return [int(string[:division]), int(string[division+1:])]