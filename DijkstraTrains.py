from re import A
from parameters import *
import heapq
from numpy import Inf

tr = []
with open("./InputDataset/trunks.csv","r") as trunks:
    tr = trunks.readlines()

sh = []
with open("./InputDataset/ship.csv","r") as ships:
    sh = ships.readlines()

#list of all stations
stations = [stat for stat in mainStations]
statIndex = dict()
for key in mainIndex:
    statIndex[key] = mainIndex[key]

for line in tr:
    s1 = clean(line.split(';')[0].split('-')[0].replace("\"",""))
    s2 = clean(line.split(';')[0].split('-')[-1].replace("\"",""))
    if s1 == s2:
        continue
    if s1 not in statIndex:
        statIndex[s1] = len(stations)
        stations.append(s1)

    if s2 not in statIndex:
        statIndex[s2] = len(stations)
        stations.append(s2)

#find distances from root following paths which minimize cost
def dijkstra(graph, root, year):
    n = len(graph)
    # set up "inf" distances
    #distance from root for each mean
    dist = [[Inf for __ in range(3)] for _ in range(n)]
    #min costs from root for each mean
    costDist = [[Inf for __ in range(3)] for _ in range(n)]
    #preceding node and mean of transport to move from preceding to actual
    prec = [[-1,-1] for _ in range(n)]
    # set up root distance
    dist[root] = [0,0,0]
    costDist[root] = [0,0,0]
    # set up visited node list
    visited = [False for _ in range(n)]
    # set up priority queue
    pq = [(0, root)]
    # while there are nodes to process
    while len(pq) > 0:
        # get the root, discard current distance
        _, u = heapq.heappop(pq)
        # if the node is visited, skip
        if visited[u]:
            continue
        # set the node to visited
        visited[u] = True

        for [next,l,t] in graph[u]:
            # if the current node's cost + cost to the node we're visiting (+ fix cost if mean changes)
            # is less than the cost of the node we're visiting on file
            # replace that cost and push the node we're visiting into the priority queue
            oldCost = newCost = 0
            for m in range(3):
                oldCost += costDist[next][m]
                newCost += costDist[u][m]

            newCost += costTrunk(t,yearIndex[year],l)
            #change of mean of transport --> fix costs
            if prec[u][1] != t:
                newCost += costs[t][yearIndex[year]][1]

            if newCost < oldCost:
                prec[next] = [u,t]
                for m in range(3):
                    dist[next][m] = dist[u][m]
                    costDist[next][m] = costDist[u][m]

                dist[next][t] += l
                costDist[next][t] += costTrunk(t,yearIndex[year],l)
                if prec[u][1] != t:
                    costDist[next][t] += costs[t][yearIndex[year]][1]
                
                costDistTot = 0
                for m in range(3):
                    costDistTot += costDist[next][m]

                heapq.heappush(pq, (costDistTot, next))

    return dist

nStaz = len(stations)

#iterate through years
for year in years:
    #adjacency list
    #for each node list of (next_node, length_trunk, mean_of_transport)
    graph = [[] for _ in range(nStaz)]

    #railway and regular road
    for line in tr:
        s1 = clean(line.split(';')[0].split('-')[0].replace("\"",""))
        s2 = clean(line.split(';')[0].split('-')[-1].replace("\"",""))
        if s1 == s2:
            continue
        y = int(line.split(';')[1])
        l = float(line.split(';')[2].replace(',','.'))

        #if year of analysis is before construction --> regular road
        if year >= y:
            #t = 2 #if we consider only road
            t = 0 #if we consider railways
        else:
            t = 2
        graph[statIndex[s1]].append([statIndex[s2],l,t])
        graph[statIndex[s2]].append([statIndex[s1],l,t])
    
    #ship (always existed)
    for line in sh:
        s1 = clean(line.split(';')[0].split('-')[0].replace("\"",""))
        s2 = clean(line.split(';')[0].split('-')[-1].replace("\"",""))
        if s1 == s2:
            continue
        l = float(line.split(';')[2].replace(',','.'))
        graph[statIndex[s1]].append([statIndex[s2],l,1])
        graph[statIndex[s2]].append([statIndex[s1],l,1])

    ##USES RAILWAYS
    with open(f"./OutputData/connections{year}.csv","w") as output:

        output.write(str(year)+";;;\n")

        totDist = [0,0,0]
        totTrips = 0
        for mainIdx in range(len(mainStations)):
            distances = dijkstra(graph,mainIdx,year)
            for otherMain in range(mainIdx+1,len(mainStations)):
                if distances[otherMain] == [Inf,Inf,Inf]:
                    continue
                output.write(mainUpper[mainIdx]+'-'+mainUpper[otherMain])
                totTrips += 1
                for m in range(3):
                    output.write(";"+str(distances[otherMain][m]).replace(".",","))
                    totDist[m] += distances[otherMain][m]
                output.write('\n')
        
        output.write("AVERAGE")
        for m in range(3):
            output.write(";"+str(totDist[m]/totTrips).replace(".",","))


    ## DOES NOT USE RAILWAYS
    ## !change t = 2 in the above code!
    # with open(f"./OutputData/connectionsNoRail.csv","w") as output:
    #     abc = 1
    # with open(f"./OutputData/connectionsNoRail.csv","a") as output:

    #     output.write(str(year))

    #     totDist = [0,0,0]
    #     totTrips = 0
    #     for mainIdx in range(len(mainStations)):
    #         distances = dijkstra(graph,mainIdx,year)
    #         for otherMain in range(mainIdx+1,len(mainStations)):
    #             if distances[otherMain] == [Inf,Inf,Inf]:
    #                 continue
    #             totTrips += 1
    #             for m in range(3):
    #                 totDist[m] += distances[otherMain][m]
        
    #     for m in range(3):
    #         output.write(";"+str(totDist[m]/totTrips).replace(".",","))
    #     output.write("\n")

    


