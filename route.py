
class Route():
    def __init__(self, id, plate, pointID2reqID,
                reqID2segment, pointID2segment, pointID2hubID, pointID2hubName, hubID2name, reqID2pickupPoint, reqID2deliveryPoint,
                timeMatrix, distMatrix, pointID2load, servingDuration, latestArrivalTime, st, en, stTime, capacity,
                forbidenPoints, maxStopPoints):
        self.id = id
        self.plate = plate
        self.reqID2segment = reqID2segment
        self.pointID2segment = pointID2segment
        self.pointID2req = pointID2reqID
        self.pointID2hubID = pointID2hubID
        self.pointID2hubName = pointID2hubName
        self.hubID2name = hubID2name
        self.reqID2pickupPoint = reqID2pickupPoint
        self.reqID2deliveryPoint = reqID2deliveryPoint
        self.timeMatrix = timeMatrix
        self.distMatrix = distMatrix
        self.pointID2load = pointID2load
        self.servingDuration = servingDuration
        self.latestArrivalTime = latestArrivalTime
        self.capacity = capacity
        self.maxStopPoints = maxStopPoints
        self.forbidenPoints = forbidenPoints

        self.pointID_lst = [st, en]
        self.hub_lst = [pointID2hubID[st], pointID2hubID[en]]
        self.req_lst = [-1, -1]
        self.acm_time = [stTime, stTime]
        self.acm_dist = [0, 0]
        self.acm_load = [0, 0]
        self.acm_hub = [0, 0]
        self.acm_vio = [0, 0]
        self.startChangeIndex = 1000

        self.prev_pointID_lst = [st, en]
        self.prev_hub_lst = [pointID2hubID[st], pointID2hubID[en]]
        self.prev_req_lst = [-1, -1]
        self.prev_acm_time = [stTime, stTime]
        self.prev_acm_dist = [0, 0]
        self.prev_acm_load = [0, 0]
        self.prev_acm_hub = [0, 0]
        self.prev_acm_vio = [0, 0]
        self.prev_startChangeIndex = 1000

    def copyCur2prev(self):
       #print('copyCur2prev')
        self.prev_pointID_lst = self.pointID_lst.copy()
        self.prev_hub_lst = self.hub_lst.copy()
        self.prev_req_lst = self.req_lst.copy()
        self.prev_acm_time = self.acm_time.copy()
        self.prev_acm_dist = self.acm_dist.copy()
        self.prev_acm_load = self.acm_load.copy()
        self.prev_acm_hub = self.acm_hub.copy()
        self.prev_acm_vio = self.acm_vio.copy()
        self.prev_startChangeIndex = self.startChangeIndex

    def copyCur2other(self,pointID_lst, hub_lst, req_lst, acm_time, acm_dist, acm_load, acm_hub, acm_vio, startChangeIndex,
                      prev_pointID_lst, prev_hub_lst, prev_req_lst, prev_acm_time, prev_acm_dist, prev_acm_load, prev_acm_hub,
                      prev_acm_vio, prev_startChangeIndex):
        #print('copyCur2other')
        self.pointID_lst = pointID_lst.copy()
        self.hub_lst = hub_lst.copy()
        self.req_lst = req_lst.copy()
        self.acm_time = acm_time.copy()
        self.acm_dist = acm_dist.copy()
        self.acm_load = acm_load.copy()
        self.acm_hub = acm_hub.copy()
        self.acm_vio = acm_vio.copy()
        self.startChangeIndex = startChangeIndex

        self.prev_pointID_lst = prev_pointID_lst.copy()
        self.prev_hub_lst = prev_hub_lst.copy()
        self.prev_req_lst = prev_req_lst.copy()
        self.prev_acm_time = prev_acm_time.copy()
        self.prev_acm_dist = prev_acm_dist.copy()
        self.prev_acm_load = prev_acm_load.copy()
        self.prev_acm_hub = prev_acm_hub.copy()
        self.prev_acm_vio = prev_acm_vio.copy()
        self.prev_startChangeIndex = prev_startChangeIndex

    def copyPrev2cur(self):
        #print('copyPrev2cur')
        self.pointID_lst = self.prev_pointID_lst.copy()
        self.hub_lst = self.prev_hub_lst.copy()
        self.req_lst = self.prev_req_lst.copy()
        self.acm_time = self.prev_acm_time.copy()
        self.acm_dist = self.prev_acm_dist.copy()
        self.acm_load = self.prev_acm_load.copy()
        self.acm_hub = self.prev_acm_hub.copy()
        self.acm_vio = self.prev_acm_vio.copy()
        self.startChangeIndex = self.prev_startChangeIndex

    def removeOneRequest(self, reqID):
        pickup_point = self.reqID2pickupPoint[reqID]
        delivery_point = self.reqID2deliveryPoint[reqID]
        if pickup_point not in self.pointID_lst or delivery_point not in self.pointID_lst:
            print('Bug in removal')
        pick_index = self.pointID_lst.index(pickup_point)
        del_index = self.pointID_lst.index(delivery_point)
        self.startChangeIndex = pick_index

        del self.pointID_lst[pick_index]
        del self.pointID_lst[del_index - 1]
        del self.hub_lst[pick_index]
        del self.hub_lst[del_index - 1]
        del self.req_lst[pick_index]
        del self.req_lst[del_index - 1]
        del self.acm_load[pick_index]
        del self.acm_load[del_index - 1]
        del self.acm_time[pick_index]
        del self.acm_time[del_index - 1]
        del self.acm_dist[pick_index]
        del self.acm_dist[del_index - 1]
        del self.acm_hub[pick_index]
        del self.acm_hub[del_index - 1]
        del self.acm_vio[pick_index]
        del self.acm_vio[del_index - 1]

    def addOneRequest(self, pickupPoint, deliveryPoint, i, j):
        if [pickupPoint, deliveryPoint] in self.pointID_lst:
            print('Bug in insertion')
        self.pointID_lst.insert(i, pickupPoint)
        self.hub_lst.insert(i, self.pointID2hubID[pickupPoint])
        self.req_lst.insert(i, self.pointID2req[pickupPoint])
        self.acm_time.insert(i, 0)
        self.acm_dist.insert(i, 0)
        self.acm_load.insert(i, 0)
        self.acm_hub.insert(i, 0)
        self.acm_vio.insert(i, 0)
        if self.startChangeIndex > i:
            self.startChangeIndex = i

        j = j + 1
        self.pointID_lst.insert(j, deliveryPoint)
        self.hub_lst.insert(j, self.pointID2hubID[deliveryPoint])
        self.req_lst.insert(j, self.pointID2req[deliveryPoint])
        self.acm_time.insert(j, 0)
        self.acm_dist.insert(j, 0)
        self.acm_load.insert(j, 0)
        self.acm_hub.insert(j, 0)
        self.acm_vio.insert(j, 0)

    def update(self):
        if self.startChangeIndex == 0:
            print('Bug startChangeIndex')

        added_vio = 0
        for i in range(self.startChangeIndex, len(self.pointID_lst)):
            cur_time = self.acm_time[i - 1]
            cur_dist = self.acm_dist[i - 1]
            cur_load = self.acm_load[i - 1]
            cur_hub = self.hub_lst[i - 1]
            cur_vio = self.acm_vio[i - 1]
            cur_point = self.pointID_lst[i - 1]
            #check time constraint
            self.acm_time[i] = cur_time + self.timeMatrix[cur_point][self.pointID_lst[i]] + self.servingDuration[cur_point]
            self.acm_dist[i] = cur_dist + self.distMatrix[cur_point][self.pointID_lst[i]]
            time_vio = self.acm_time[i] - self.latestArrivalTime[self.pointID_lst[i]]
            if time_vio > 0:
                added_vio = added_vio + time_vio

            #check capacity constraint
            self.acm_load[i] = cur_load + self.pointID2load[self.pointID_lst[i]]
            cap_vio = self.acm_load[i] - self.capacity
            if cap_vio > 0:
                added_vio = added_vio + cap_vio

            #check nb stop hubs
            hubID = self.pointID2hubID[self.pointID_lst[i]]
            self.hub_lst[i] = hubID
            hubName = self.hubID2name[hubID]
            cur_hubName = self.hubID2name[cur_hub]
            hub1 = str(hubName).replace('fm-','')
            hub1 = hub1.replace('lm-', '')
            hub2 = str(cur_hubName).replace('fm-', '')
            hub2 = hub2.replace('lm-', '')
            if hub1 != hub2:
                self.acm_hub[i] = self.acm_hub[i-1] + 1
            else:
                self.acm_hub[i] = self.acm_hub[i-1]
            length_vio = self.acm_hub[i] - self.maxStopPoints
            if length_vio > 0:
                added_vio = added_vio + length_vio

            #check forbiden point constraint
            if self.pointID2hubID[self.pointID_lst[i]] in self.forbidenPoints:
                added_vio = added_vio + 10

            #done check
            self.acm_vio[i] = cur_vio + added_vio
            self.req_lst[i] = self.pointID2req[self.pointID_lst[i]]

        self.startChangeIndex = 1000

    def getViolation(self):
        return self.acm_vio[len(self.pointID_lst) - 1]

    def getTimeObjective(self):
        return self.acm_time[len(self.pointID_lst) - 1] - self.acm_time[0]
    def getDistObjective(self):
        return self.acm_dist[len(self.pointID_lst) - 1]
    def getVehicleObjective(self):
        if len(self.pointID_lst) > 2:
            return 1
        else:
            return 0

    def getPrevTimeObjective(self):
        return self.prev_acm_time[len(self.prev_pointID_lst) - 1] - self.prev_acm_time[0]

    def getPrevDistObjective(self):
        return self.prev_acm_dist[len(self.prev_pointID_lst) - 1]

    def getPrevVehicleObjective(self):
        if len(self.prev_pointID_lst) > 2:
            return 1
        else:
            return 0

    def toString(self):
        hubName = self.pointID2hubName[self.pointID_lst[0]]
        s = 'Truck ' + str(self.id) + ': ' + str(hubName) + ' -> '
        for i in range(1, len(self.pointID_lst) - 1):
            hubName = self.pointID2hubName[self.pointID_lst[i]]
            s = s + str(hubName) + ' -> '

        hubName = self.pointID2hubName[self.pointID_lst[len(self.pointID_lst) - 1]]
        s = s + str(hubName)
        print(s)
        print('acm_time: ', self.acm_time)
        print('acm_load: ', self.acm_load)
        print('acm_dist: ', self.acm_dist)
        print('==================')

    def sortingRequest(self):
        route_len = len(self.pointID_lst)
        if route_len <= 2:
            return
        k = 1
        while k < route_len-1:
            point1 = self.pointID_lst[k]
            hubName1 = str(self.pointID2hubName[point1])
            hubID1 = str(self.pointID2hubID[point1])
            acm_hub1 = self.acm_hub[k]
            changedHub = 0
            firstDropIdx = k
            if self.pointID2load[point1] > 0:
                firstDropIdx = k - 1
            for i in range(k+1, route_len - 1):
                point2 = self.pointID_lst[i]
                hubName2 = str(self.pointID2hubName[point2])
                hubID2 = str(self.pointID2hubID[point2])
                acm_hub2 = self.acm_hub[i]
                if hubID2 != hubID1 or acm_hub2 != acm_hub1:
                    break
                if hubName2 != hubName1:
                    changedHub = 1
                if changedHub == 1 and i > k + 1:
                    if hubName2 == hubName1:
                        del self.pointID_lst[i]
                        self.pointID_lst.insert(firstDropIdx+1, point2)
                        if self.pointID2load[point2] < 0:
                            firstDropIdx = self.pointID_lst.index(point2) - 1
            k = k + 1
        self.startChangeIndex = 1
        self.update()






