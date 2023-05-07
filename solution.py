from copy import deepcopy
class Solution():
    def __init__(self, route_lst, reqID2status, reqID2route, nbServedReqs, nbUsedTrucks, totalTravelTime, totalDistance, totalCapacity):
        self.route_lst = deepcopy(route_lst)
        self.reqID2status = deepcopy(reqID2status)
        self.reqID2route = deepcopy(reqID2route)
        self.nbServedReqs = deepcopy(nbServedReqs)
        self.nbUsedTrucks = deepcopy(nbUsedTrucks)
        self.totalTravelTime = deepcopy(totalTravelTime)
        self.totalDistance = deepcopy(totalDistance)
        self.totalCapacity = totalCapacity

    def copy(self, route_lst, reqID2status, reqID2route):
        rID2route = {}
        for i in range(len(route_lst)):
            route_lst[i].copyCur2other(self.route_lst[i].pointID_lst, self.route_lst[i].hub_lst, self.route_lst[i].req_lst,
                              self.route_lst[i].acm_time, self.route_lst[i].acm_dist, self.route_lst[i].acm_load,
                              self.route_lst[i].acm_hub, self.route_lst[i].acm_vio, self.route_lst[i].startChangeIndex,
                              self.route_lst[i].prev_pointID_lst, self.route_lst[i].prev_hub_lst,
                              self.route_lst[i].prev_req_lst, self.route_lst[i].prev_acm_time,  self.route_lst[i].prev_acm_dist,
                              self.route_lst[i].prev_acm_load, self.route_lst[i].prev_acm_hub,
                              self.route_lst[i].prev_acm_vio, self.route_lst[i].prev_startChangeIndex)
            for k , v in self.reqID2route.items():
                if v.id == route_lst[i].id:
                    rID2route[k] = route_lst[i]
        for k in self.reqID2status:
            reqID2status[k] = self.reqID2status[k]

        reqID_lst = [k for k, v in reqID2route.items()]
        for i in range(len(reqID_lst)):
            del reqID2route[reqID_lst[i]]
        for k, v in rID2route.items():
            reqID2route[k] = v


