import numpy as np
import re

#clean strings to avoid mismatches
def clean(s):
    word = ""
    i = 0
    while i in range(len(s)):
        if s[i] == '(':
            while i in range(len(s)) and s[i] != ')':
                i += 1
        else:
            word += s[i]   
        i += 1 
    word = re.sub(r"[^a-zA-Z]","",word)
    word = word.lower()
    return word

years = [1871,1891,1911]
yearIndex = {}
for y in range(len(years)):
    yearIndex[years[y]] = y

means = ['R','S','RR']#railway, ship, regular road

#fix and variable costs
costs = np.zeros((len(means),len(years),2))
with open("costs.csv") as f:
    s = f.readlines()
    for m in range(len(means)):
        for mode in range(2):
            line = s[2*m+mode][:-1].split(';')
            for y in range(len(years)):
                costs[m][y][mode] = float(line[y].replace(',','.'))

#lists of main stations
#good-looking
mainUpper = []
#after clean
mainStations = []
mainIndex = {}
with open("mainStations.csv","r") as f:
    s = f.readlines()
    for l in range(len(s)):
        line = s[l]
        Stat = line[1:-2]
        mainUpper.append(Stat)
        mainStations.append(clean(Stat))
        mainIndex[clean(Stat)] = l

#length * cost
def costTrunk(m,y,l):
    return l*costs[m][y][1]

##DOES NOT USE RAILWAYS
# with open(f"connectionsNoRail.csv","w") as output:
#     a = 1