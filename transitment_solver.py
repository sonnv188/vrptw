from IOfunction import IOfunction
from DataSelection import DataPreparation
from solution import Solution
from route import Route
import random
import time
import math
import numpy as np

def initWeighOfOperator(nbInsertion, nbRemoval):
    rm_weights = [1/nbRemoval for i in range(nbRemoval)]
    ins_weights = [1/nbInsertion for i in range(nbInsertion)]
    ins_used = [0 for i in range(nbInsertion)]
    rm_used = [0 for i in range(nbRemoval)]
    ins_score = [0 for i in range(nbInsertion)]
    rm_score = [0 for i in range(nbRemoval)]
    return rm_weights, ins_weights, ins_used, rm_used, ins_score, rm_score

def chooseOperator(weight):
    if 0 in weight:
        n = len(weight)
        weight = [1/n for i in range(n)]
    n = len(weight)
    s = []
    s.append(0 + weight[0])
    for i in range(1, n):
        s.append(s[i-1] + weight[i])
    r = s[n-1] * random.random()

    if r >= 0 and r <= s[0]:
        return 0;
    for i in range(1, n):
        if r > s[i - 1] and r <= s[i]:
            return i

    return -1

def updateProbabilities(nbInsertion, ins_weights, ins_used, ins_score, nbRemoval, rm_weights, rm_used, rm_score):
    for i in range(0, nbInsertion):
        if ins_used[i] != 0:
            ins_weights[i] = max(0, ins_weights[i] * 0.9 + 0.1 * ins_score[i] / ins_used[i]);
    for i in range(0, nbRemoval):
        if rm_used[i] != 0:
            rm_weights[i] = max(0, rm_weights[i] * 0.9 + 0.1 * rm_score[i] / rm_used[i]);
    return rm_weights, ins_weights

def compareSolution(best_nbTrucks, best_travelTime, best_distance):
    new_nbTrucks = 0
    new_travelTime = 0
    for route in route_lst:
        new_nbTrucks = new_nbTrucks + route.getVehicleObjective()
        new_travelTime = new_travelTime + route.getTimeObjective()
        new_distance = new_travelTime + route.getDistObjective()
    if new_nbTrucks < best_nbTrucks:
        return True, new_nbTrucks, new_travelTime, new_distance
    else:
        if new_nbTrucks == best_nbTrucks and new_distance < best_distance:
            return True, new_nbTrucks, new_travelTime, new_distance
    return False, best_nbTrucks, best_travelTime, best_distance

def addTruck2RequestAtFirstPosiblePosition():
    #print('0. addTruck2RequestAtFirstPosiblePosition')
    for req in reqs:
        reqID = req[0]
        if reqID2status[reqID] == 1:
            continue
        pickPoint = reqID2pickupPoint[reqID]
        delPoint = reqID2deliveryPoint[reqID]

        isInserted = False
        for route in route_lst:
            for i in range(1, len(route.pointID_lst)):
                for j in range(i, len(route.pointID_lst)):
                    route.addOneRequest(pickPoint, delPoint, i, j)
                    route.update()
                    if route.getViolation() > 0:
                        route.copyPrev2cur()
                    else:
                        route.copyCur2prev()
                        isInserted = True
                        reqID2status[reqID] = 1
                        reqID2route[reqID] = route
                        break
                if isInserted == True:
                    break
            if isInserted == True:
                break

def addRequest2TruckAtFirstPosiblePosition():
    #print('1. addRequest2TruckAtFirstPosiblePosition')
    for route in route_lst:
        for req in reqs:
            reqID = req[0]
            if reqID2status[reqID] == 1:
                continue
            pickPoint = reqID2pickupPoint[reqID]
            delPoint = reqID2deliveryPoint[reqID]

            isInserted = False
            for i in range(1, len(route.pointID_lst)):
                for j in range(i, len(route.pointID_lst)):
                    route.addOneRequest(pickPoint, delPoint, i, j)
                    route.update()
                    if route.getViolation() > 0:
                        route.copyPrev2cur()
                    else:
                        route.copyCur2prev()
                        isInserted = True
                        reqID2status[reqID] = 1
                        reqID2route[reqID] = route
                        break
                if isInserted == True:
                    break

def addTruck2RequestAtBestPosiblePosition():
    #print('2. addTruck2RequestAtBestPosiblePosition')
    for req in reqs:
        reqID = req[0]
        if reqID2status[reqID] == 1:
            continue
        pickPoint = reqID2pickupPoint[reqID]
        delPoint = reqID2deliveryPoint[reqID]

        best_nbTruck = 1000
        best_travelTime = 1e10
        best_distance = 1e10
        best_i = -1
        best_j = -1
        best_route = route_lst[0]
        for route in route_lst:
            for i in range(1, len(route.pointID_lst)):
                for j in range(i, len(route.pointID_lst)):
                    route.addOneRequest(pickPoint, delPoint, i, j)
                    route.update()
                    if route.getViolation() > 0:
                        route.copyPrev2cur()
                    else:
                        isBest, nbTrucks, totalTravelTime, totalDistance = compareSolution(best_nbTruck, best_travelTime, best_distance)
                        if isBest == True:
                            best_i = i
                            best_j = j
                            best_route = route
                            best_nbTruck = nbTrucks
                            best_travelTime = totalTravelTime
                            best_distance = totalDistance
                        route.copyPrev2cur()
        if best_i != -1:
            best_route.addOneRequest(pickPoint, delPoint, best_i, best_j)
            best_route.update()
            best_route.copyCur2prev()
            reqID2status[reqID] = 1
            reqID2route[reqID] = best_route

def addRequest2TruckAtBestPosiblePosition():
    #print('3. addRequest2TruckAtBestPosiblePosition')
    for route in route_lst:
        best_nbTruck = 1000
        best_travelTime = 1e10
        best_distance = 1e10
        best_i = -1
        best_j = -1
        best_reqID = -1
        for req in reqs:
            reqID = req[0]
            if reqID2status[reqID] == 1:
                continue
            pickPoint = reqID2pickupPoint[reqID]
            delPoint = reqID2deliveryPoint[reqID]
            for i in range(1, len(route.pointID_lst)):
                for j in range(i, len(route.pointID_lst)):
                    route.addOneRequest(pickPoint, delPoint, i, j)
                    route.update()
                    if route.getViolation() > 0:
                        route.copyPrev2cur()
                    else:
                        isBest, nbTrucks, totalTravelTime, totalDistance = compareSolution(best_nbTruck, best_travelTime, best_distance)
                        if isBest == True:
                            best_i = i
                            best_j = j
                            best_reqID = reqID
                            best_nbTruck = nbTrucks
                            best_travelTime = totalTravelTime
                            best_distance = totalDistance
                        route.copyPrev2cur()
        if best_i != -1:
            pickPoint = reqID2pickupPoint[best_reqID]
            delPoint = reqID2deliveryPoint[best_reqID]
            route.addOneRequest(pickPoint, delPoint, best_i, best_j)
            route.update()
            route.copyCur2prev()
            reqID2status[best_reqID] = 1
            reqID2route[best_reqID] = route

def removeRandomReqs(nbRemoval):
    # print('0. removeRandomReqs')
    if len(reqID2route) == 0:
        return
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    reqID_lst = [k for k, v in reqID2route.items()]
    random.shuffle(reqID_lst)
    for reqID in reqID_lst:
        route = reqID2route[reqID]
        route.removeOneRequest(reqID)
        cnt = cnt + 1
        removedReqID.add(reqID)
        routeChanged.add(route)
        if cnt >= nbRemoval:
            break
    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

def removeWorseReqs(nbRemoval):
    # print('1. removeWorseReqs')
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    r_lst = [v for k, v in reqID2route.items()]
    while len(removedReqID) < len(reqID2route):
        max_pointID = -1
        max_D = -1
        max_route = route_lst[0]
        for r in r_lst:
            length = len(r.pointID_lst)
            if length <= 2:
                continue
            for i in range(1, length-1):
                d = distMatrix[r.pointID_lst[i-1]][r.pointID_lst[i]] \
                    + distMatrix[r.pointID_lst[i]][r.pointID_lst[i+1]] \
                    - distMatrix[r.pointID_lst[i-1]][r.pointID_lst[i+1]]
                if d > max_D:
                    max_D = d
                    max_pointID = r.pointID_lst[i]
                    max_route = r
        if max_D != -1:
            reqID = pointID2reqID[max_pointID]
            max_route.removeOneRequest(reqID)
            cnt = cnt + 1
            removedReqID.add(reqID)
            routeChanged.add(max_route)
        if cnt >= nbRemoval:
            break

    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

def removeAllRoute(nbRemoval):
    # print('2. removeAllRoute')
    if len(reqID2route) == 0:
        return
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    route_key = np.random.permutation(len(route_lst))
    for i in route_key:
        route = route_lst[i]
        req_lst = [k for k, v in reqID2route.items() if v == route]
        for reqID in req_lst:
            route.removeOneRequest(reqID)
            cnt = cnt + 1
            removedReqID.add(reqID)
            routeChanged.add(route)

        if cnt >= nbRemoval:
            break
    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

def removeShortestRoute(nbRemoval):
    # print('3. removeShortestRoute')
    if len(reqID2route) == 0:
        return
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    while True:
        if cnt >= nbRemoval or len(removedReqID) == len(reqID2route):
            break
        min_routeLen = 1000
        min_route = route_lst[0]
        for r in route_lst:
            routeLen = len(route_lst[0].pointID_lst)
            if routeLen <= 2:
                continue
            if min_routeLen > routeLen:
                min_routeLen = routeLen
                min_route = r
        if min_routeLen != 1000:
            req_lst = [k for k, v in reqID2route.items() if v == min_route]
            for reqID in req_lst:
                min_route.removeOneRequest(reqID)
                cnt = cnt + 1
                removedReqID.add(reqID)
                routeChanged.add(min_route)
                # if cnt >= nbRemoval:
                #     break
        else:
            break
    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

def removeLongestRoute(nbRemoval):
    # print('4. removeLongestRoute')
    if len(reqID2route) == 0:
        return
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    while True:
        if cnt >= nbRemoval or len(removedReqID) == len(reqID2route):
            break
        max_routelen = -1
        max_route = route_lst[0]
        for r in route_lst:
            routeLen = len(route_lst[0].pointID_lst)
            if routeLen <= 2:
                continue
            if max_routelen < routeLen:
                max_routelen = routeLen
                max_route = r
        if max_routelen != -1:
            req_lst = [k for k, v in reqID2route.items() if v == max_route]
            for reqID in req_lst:
                max_route.removeOneRequest(reqID)
                cnt = cnt + 1
                removedReqID.add(reqID)
                routeChanged.add(max_route)
        else:
            break

    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

def removeReqsOnSegment(nbRemoval):
    # print('5. removeReqsOnSegment')
    if len(reqID2route) == 0:
        return
    cnt = 0
    routeChanged = set()
    removedReqID = set()
    visited_d = set()
    while True:
        if cnt >= nbRemoval or len(removedReqID) == len(reqID2route):
            break
        max_nb = -1
        max_d = Demand[0, 0]
        for d in Demand.keys():
            if len(Demand[d].requests) > max_nb and d not in visited_d:
                max_nb = len(Demand[d].requests)
                max_d = d
        visited_d.add(max_d)
        for req in Demand[max_d].requests:
            reqID = req[0]
            if reqID2status[reqID] == 0:
                continue
            route = reqID2route[reqID]
            cnt = cnt + 1
            route.removeOneRequest(reqID)
            removedReqID.add(reqID)
            routeChanged.add(route)
            if cnt >= nbRemoval:
                break
    for reqID in removedReqID:
        del reqID2route[reqID]
        reqID2status[reqID] = 0
    for route in routeChanged:
        route.update()
        route.copyCur2prev()

    removeShortestRoute(nbRemoval/2)

def alns(maxIter, maxTime, maxStable, score1, score2, score3):
    nbInsertionOp = 2
    nbRemovalOp = 6
    removalRateTop = 0.45
    removalRateBottom = 0.05
    temperature = 200
    coolingRate = 0.9995


    rm_weights, ins_weights, ins_used, rm_used, ins_score, rm_score = initWeighOfOperator(nbInsertionOp, nbRemovalOp)

    servedReqs = [k for k, v in reqID2status.items() if v == 1]
    nbServedReqs = len(servedReqs)
    nbUsedTrucks = 0
    totalTravelTime = 0
    totalDistance = 0
    totalCapacity = 0
    for route in route_lst:
        nbUsedTrucks = nbUsedTrucks + route.getVehicleObjective()
        totalTravelTime = totalTravelTime + route.getTimeObjective()
        totalDistance = totalDistance + route.getDistObjective()
        totalCapacity = totalCapacity + route.capacity
    best_solution = Solution(route_lst, reqID2status, reqID2route, nbServedReqs, nbUsedTrucks, totalTravelTime, totalDistance, totalCapacity)

    it = 0
    cur_time = time.time()
    cnt = 0
    isBad = 0
    while it < maxIter and time.time() - cur_time < maxTime:
        servedReqs = [k for k, v in reqID2status.items() if v == 1]
        nbServedReqs = len(servedReqs)
        nbUsedTrucks = 0
        totalTravelTime = 0
        totalDistance = 0
        totalCapacity = 0
        for route in route_lst:
            nbUsedTrucks = nbUsedTrucks + route.getVehicleObjective()
            totalTravelTime = totalTravelTime + route.getTimeObjective()
            totalDistance = totalDistance + route.getDistObjective()
            totalCapacity = totalCapacity + route.capacity
        cur_solution = Solution(route_lst, reqID2status, reqID2route, nbServedReqs, nbUsedTrucks, totalTravelTime, totalDistance, totalCapacity)

        # for k in reqID2route:
        #     if reqID2status[k] == 0:
        #         print('bug with reqID = ', k, 'route = ', route.id)
        ins_op = chooseOperator(ins_weights)
        rm_op = chooseOperator(rm_weights)
        if cnt >= maxStable:
            # print('====== restart ======')
            n = len(reqID2route)
            removeRandomReqs(n)
            cnt = 0
        else:
            nbRemoval = len(reqs) * removalRateBottom + random.randint(0, (int)(
                len(reqs) * (removalRateTop - removalRateBottom)))
            if rm_op == 0:
                removeRandomReqs(nbRemoval)
            elif rm_op == 1:
                removeAllRoute(nbRemoval)
            elif rm_op == 2:
                removeReqsOnSegment(nbRemoval)
            elif rm_op == 3:
               removeWorseReqs(nbRemoval)
            elif rm_op == 4:
               removeShortestRoute(nbRemoval)
            elif rm_op == 5:
               removeLongestRoute(nbRemoval)

        if ins_op == 0:
            addTruck2RequestAtBestPosiblePosition()
        elif ins_op == 1:
            addRequest2TruckAtBestPosiblePosition()
        # elif ins_op == 2:
        #     addTruck2RequestAtFirstPosiblePosition()
        # elif ins_op == 3:
        #     addRequest2TruckAtFirstPosiblePosition()

        servedReqs = [k for k, v in reqID2status.items() if v == 1]
        new_nbServedReqs = len(servedReqs)
        new_nbUsedTrucks = 0
        new_totalTravelTime = 0
        new_totalDistance = 0
        new_totalCapacity = 0
        for route in route_lst:
            new_nbUsedTrucks = new_nbUsedTrucks + route.getVehicleObjective()
            new_totalTravelTime = new_totalTravelTime + route.getTimeObjective()
            new_totalDistance = new_totalDistance + route.getDistObjective()
            new_totalCapacity = new_totalCapacity + route.capacity
        if (new_nbServedReqs > cur_solution.nbServedReqs)\
                or (new_nbServedReqs == cur_solution.nbServedReqs and new_nbUsedTrucks < cur_solution.nbUsedTrucks)\
                or (new_nbServedReqs == cur_solution.nbServedReqs and new_nbUsedTrucks == cur_solution.nbUsedTrucks
                    and new_totalDistance < cur_solution.totalDistance):
            if (new_nbServedReqs > best_solution.nbServedReqs) \
                    or (new_nbServedReqs == best_solution.nbServedReqs and new_nbUsedTrucks < best_solution.nbUsedTrucks) \
                    or (new_nbServedReqs == best_solution.nbServedReqs and new_nbUsedTrucks == best_solution.nbUsedTrucks
                        and new_totalDistance < best_solution.totalDistance):
                best_solution = Solution(route_lst, reqID2status, reqID2route,
                                         new_nbServedReqs, new_nbUsedTrucks, new_totalTravelTime, new_totalDistance, new_totalCapacity)
                ins_score[ins_op] = ins_score[ins_op] + score1
                rm_score[rm_op] = rm_score[rm_op] + score1
                cnt = 0
                isBad = 0
                # print('best solution: new_nbServedReqs = ',
                #       new_nbServedReqs, ', new_nbUsedTrucks = ', new_nbUsedTrucks, ', new_totalTravelTime = ', new_totalDistance)
            else:
                isBad = isBad + 1
                ins_score[ins_op] = ins_score[ins_op] + score2
                rm_score[rm_op] = rm_score[rm_op] + score2
                # print('cur solution: new_nbServedReqs = ',
                #       new_nbServedReqs, ', new_nbUsedTrucks = ', new_nbUsedTrucks, ', new_totalTravelTime = ',
                #       new_totalDistance)
        else:
            isBad = isBad + 1
            slack_time = new_totalDistance - cur_solution.totalDistance
            # print('slack = ', slack_time, ', tem = ', temperature)
            if temperature != 0 and slack_time < 10000 and slack_time > -10000:
                v = math.exp(-(slack_time) / temperature);
                temperature = temperature * coolingRate
                r = random.random()
                if r >= v:
                    # print('back solution')
                    best_solution.copy(route_lst, reqID2status, reqID2route)
                    ins_score[ins_op] = ins_score[ins_op] + score3
                    rm_score[rm_op] = rm_score[rm_op] + score3
                    cnt = cnt + 1

        ins_used[ins_op] = ins_used[ins_op] + 1
        rm_used[rm_op] = rm_used[rm_op] + 1
        if isBad < maxStable:
            updateProbabilities(nbInsertionOp, ins_weights, ins_used, ins_score, nbRemovalOp, rm_weights, rm_used, rm_score)
            # print(rm_weights)
        else:
            rm_weights, ins_weights, ins_used, rm_used, ins_score, rm_score = initWeighOfOperator(nbInsertionOp, nbRemovalOp)
            isBad = 0
        it = it + 1
    best_solution.copy(route_lst, reqID2status, reqID2route)
    return route_lst, reqID2status, reqID2route


best_D = 1e10
best_trucks = 10000
best_index = -1
best_Cap = 1000000
nbIter = 500
limitedTime = 900
maxStable = 30
for t in range(0, 10):
    #read excel input file
    io = IOfunction()

    inputJsonFile = "./data/json/input/2023-04-17-input-MB.json"
    hubName2hubID, hubID2name, T, D, trucks, reqs = io.InputJson(inputJsonFile)
    outputFilename = "./data/json/output/2023-04-17-output-MB.xlsx"

    if len(reqs) < 50:
        nbIter = 5000
        maxStable = 50

    # inputFilename = './data/input-2022-12-01-13h-MB.xlsx'
    # outputFilename = "./data/output-2022-12-01-13h-MB-" + str(t) + ".xlsx"
    # hubName2hubID, hubID2name, T, D, trucks, reqs = io.InputExcel(inputFilename)

    #prepare data for opt model
    dp = DataPreparation()
    points, truckID2startPoint, truckID2endPoint, truckID2startTime, pointID2reqID, \
    pointID2hubID, pointID2hubName, pointID2segment, pointID2load, reqID2segment, \
    reqID2status, reqID2pickupPoint, reqID2deliveryPoint, Demand, \
    servingDuration, latestArrivalTime, timeMatrix, distMatrix = dp.prepareData(hubName2hubID, T, D, trucks, reqs)

    route_lst = []
    for i in range(len(trucks)):
        truck_id = trucks[i][0]
        route = Route(truck_id, trucks[i][1], pointID2reqID,
                    reqID2segment, pointID2segment, pointID2hubID, pointID2hubName, hubID2name, reqID2pickupPoint, reqID2deliveryPoint,
                    timeMatrix, distMatrix, pointID2load, servingDuration, latestArrivalTime, truckID2startPoint[truck_id],
                    truckID2endPoint[truck_id], truckID2startTime[truck_id], trucks[i][5], trucks[i][6], trucks[i][7])
        route_lst.append(route)

    reqID2route = {}

    cnt = addRequest2TruckAtFirstPosiblePosition()

    #print('nb reqs: ', len(reqs), ',init inserted reqs:  ', cnt)
    best_route_lst, best_reqID2status, best_reqID2route = alns(nbIter, limitedTime, maxStable, 3, 1, -1)

    servedReqs = [k for k, v in best_reqID2status.items() if v == 1]
    best_nbUsedTrucks = 0
    best_totalDistance = 0
    best_totalCapacity = 0
    for route in best_route_lst:
        best_nbUsedTrucks = best_nbUsedTrucks + route.getVehicleObjective()
        best_totalDistance = best_totalDistance + route.getDistObjective()
        best_totalCapacity = best_totalCapacity + route.capacity

    # print('nbServedReqs = ', len(servedReqs), ', nbUsedTrucks = ', best_nbUsedTrucks, ', travelTime = ', best_totalDistance)
    # for i in range(len(best_route_lst)):
    #     print(best_route_lst[i].toString())
    # for route in best_route_lst:
    #     route.sortingRequest()
    # print("done")
    # io.print2excel(best_route_lst, len(servedReqs), best_nbUsedTrucks, best_totalDistance, pointID2hubID, pointID2hubName, hubID2name, pointID2reqID, pointID2load, './data/output-test-2.xlsx')
    if (best_trucks > best_nbUsedTrucks) or (best_trucks == best_nbUsedTrucks and best_D > best_totalDistance)\
            or (best_trucks == best_nbUsedTrucks and best_D == best_totalDistance and best_Cap > best_totalCapacity):
        best_trucks = best_nbUsedTrucks
        best_D = best_totalDistance
        best_Cap = best_totalCapacity
        best_index = t
        io.print2excel(best_route_lst, len(servedReqs), best_nbUsedTrucks, best_totalDistance, best_totalCapacity,
                       pointID2hubID, pointID2hubName, hubID2name, pointID2reqID, pointID2load, outputFilename)

with open('./data/json/bestFile.txt', 'a') as f:
    temp = "Best index: " + str(best_index) + ", best_trucks: " + str(best_trucks) + ", best_D: " + str(best_D) + ", " + outputFilename + "\n"
    f.write(temp)
