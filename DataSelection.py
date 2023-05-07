from route import Route
class DemandOnSegment:
    # store total amount of boxes and list of box requests on a segment (fromPoint, toPoint)
    def __init__(self, id, fromPoint, toPoint):
        self.id = id
        self.demand = 0
        self.fromPoint = fromPoint
        self.toPoint = toPoint
        self.requests = []

    def AddRequestBox(self, req):
        # req is a request struct: req[0] is the id, req[1], req[2] are fromPoint, toPoint; req[3] = qty
        # print('AddRequestBox', req)
        if self.fromPoint != req[1] or self.toPoint != req[2]:
            # print('AddRequestBox BUG??')
            return False
        self.requests.append(req)
        self.demand += req[3]

    def RemoveRequestBox(self, req):
        # print('RemoveRequestBox', req)
        if self.fromPoint != req[1] or self.toPoint != req[2]:
            # print('RemoveRequestBox BUG??')
            return False
        self.requests.remove(req)
        self.demand -= req[3]

    def ToString(self):
        s = '[' + str(self.fromPoint) + ' -> ' + str(self.toPoint) + ' QTY = ' + str(self.demand) + ']'
        for r in self.requests:
            s = s + '(' + str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + ',' + str(r[3]) + ') '
        return s

class DataPreparation:
    def __init__(self):
        print('DataPreparation')
    def prepareData(self, hubName2hubID, T, D, trucks, reqs):
        # print('Aggregate data')
        points = []
        truckID2startPoint = {}
        truckID2endPoint = {}
        truckID2startTime = {}
        pointID2reqID = {}
        pointID2hubID = {}
        pointID2hubName = {}
        pointID2segment = {}
        pointID2load = {}
        reqID2segment = {}
        reqID2status = {}
        reqID2pickupPoint = {}
        reqID2deliveryPoint = {}
        servingDuration = {}
        latestArrivalTime = {}

        # make start point and end point of each truck
        id = -1
        for truck in trucks:
            id = id + 1
            points.append(id)
            servingDuration[id] = 0
            truckID2startPoint[truck[0]] = id
            truckID2startTime[truck[0]] = truck[3]
            latestArrivalTime[id] = truck[4]
            pointID2hubID[id] = truck[2]
            pointID2hubName[id] = truck[8]
            pointID2load[id] = 0
            pointID2reqID[id] = -1

            id = id + 1
            points.append(id)
            servingDuration[id] = 0
            truckID2endPoint[truck[0]] = id
            latestArrivalTime[id] = truck[4]
            pointID2hubID[id] = truck[2]
            pointID2hubName[id] = truck[8]
            pointID2load[id] = 0
            pointID2reqID[id] = -1

        for req in reqs:
            id = id + 1
            points.append(id)
            pointID2reqID[id] = req[0]
            reqID2pickupPoint[req[0]] = id
            servingDuration[id] = req[4]
            latestArrivalTime[id] = req[6]
            pointID2hubID[id] = req[1]
            pointID2hubName[id] = req[8]
            pointID2load[id] = req[3]

            id = id + 1
            points.append(id)
            pointID2reqID[id] = req[0]
            reqID2deliveryPoint[req[0]] = id
            servingDuration[id] = req[5]
            latestArrivalTime[id] = req[7]
            pointID2hubID[id] = req[2]
            pointID2hubName[id] = req[9]
            pointID2load[id] = 0 - req[3]

        nbHubs = len(hubName2hubID)
        Demand = {}
        segment_id = 0
        for i in range(0, nbHubs):
            for j in range(0, nbHubs):
                Demand[i, j] = DemandOnSegment(segment_id, i, j)
                segment_id = segment_id + 1

        for req in reqs:
            Demand[req[1], req[2]].AddRequestBox(req)
            segment_id = Demand[req[1], req[2]].id
            req_id = req[0]
            reqID2segment[req_id] = segment_id
            reqID2status[req_id] = 0
            pickupPoint = reqID2pickupPoint[req_id]
            deliveryPoint = reqID2deliveryPoint[req_id]
            pointID2segment[pickupPoint] = segment_id
            pointID2segment[deliveryPoint] = segment_id

        nbPoints = len(points)
        timeMatrix = [[0 for i in range(nbPoints)] for j in range(nbPoints)]
        distMatrix = [[0 for i in range(nbPoints)] for j in range(nbPoints)]
        for i in range(0, nbPoints):
            for j in range(0, nbPoints):
                t = 0
                d = 0
                if i != j:
                    pickHubID = pointID2hubID[i]
                    delHubID = pointID2hubID[j]
                    t = T[pickHubID][delHubID]
                    d = D[pickHubID][delHubID]

                timeMatrix[i][j] = t
                distMatrix[i][j] = d

        return points, truckID2startPoint, truckID2endPoint, truckID2startTime, pointID2reqID, \
               pointID2hubID, pointID2hubName, pointID2segment, pointID2load, reqID2segment, \
               reqID2status, reqID2pickupPoint, reqID2deliveryPoint, Demand, \
               servingDuration, latestArrivalTime, timeMatrix, distMatrix

