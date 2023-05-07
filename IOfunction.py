import pandas as pd
import datetime
import json
from utilities import Utilities
import openpyxl

class IOfunction:
    def __init__(self):
        self.util = Utilities()

    def InputJson(self, filename):
        f = open(filename)
        data = json.load(f)
        df = data['Hub']
        hubID2name = {}
        hubName2hubID = {}
        for i in range(len(df)):
            # print(df[i]['HubID'], df[i]['Name'])
            h = df[i]['HubID']
            hubName2hubID[h] = i
            hubID2name[i] = h

        df = data['DistanceTime']
        n = len(hubName2hubID)

        # read distance
        T = [[0 for i in range(n)] for j in range(n)]
        D = [[0 for i in range(n)] for j in range(n)]
        for k in range(len(df)):
            fromHub = self.util.removeSubTitle(df[k]['FromHub'])
            i = hubName2hubID[fromHub]
            toHub = self.util.removeSubTitle(df[k]['ToHub'])
            j = hubName2hubID[toHub]
            t = df[k]['TravelTime']
            d = df[k]['Distance']
            # print(k, ': fromHub = ', fromHub, 'toHub = ', toHub, ' d(', i, ',', j, ') = ', d)
            T[i][j] = t
            D[i][j] = d

        # read trucks
        df = data['truck']
        trucks = []
        truckID2forbidenPoints = {}
        for i in range(len(df)):
            truckPlate = df[i]['truckID']
            cap = df[i]['Capacity']
            stWorkingTime = df[i]['StartWorkingTime']
            endWorkingTime = df[i]['EndWorkingTime']
            originLoc = df[i]['location']
            stLocation = hubName2hubID[self.util.removeSubTitle(originLoc)]
            forbidenPoints = []
            if pd.isna(df[i]['ForbidenPoint']) == False:
                s = str(df[i]['ForbidenPoint']).split(',')
                for j in range(len(s)):
                    h = s[j].strip()
                    h = self.util.removeSubTitle(h)
                    forbidenPoints.append(hubName2hubID[h])
            truckID2forbidenPoints[i] = forbidenPoints
            maxStopPoints = df[i]['MaxStopPoints']
            trucks.append([i, truckPlate, stLocation, int(self.util.DateTime2Int(stWorkingTime)),
                           int(self.util.DateTime2Int(endWorkingTime)), cap, forbidenPoints, maxStopPoints, originLoc])

        # read requests
        df = data['request']
        requests = []

        for i in range(len(df)):
            id = df[i]['RequestID']
            fHub_origin = df[i]['PickupPoint']
            tHub_origin = df[i]['DeliveryPoint']
            fHub = self.util.removeSubTitle(fHub_origin)
            tHub = self.util.removeSubTitle(tHub_origin)
            # lao cai, son la bo qua
            if ("caugiay" in str(fHub) and ("sonla" in str(tHub) or "laocai" in str(tHub))) \
                    or ("sonla" in str(fHub) or "laocai" in str(fHub)):
                continue
            if "sonla" in str(tHub) or "laocai" in str(tHub):
                tHub = "hub-caugiay"
            fromPoint = hubName2hubID[fHub]
            toPoint = hubName2hubID[tHub]
            pickTime = df[i]['PickupDateTime']
            deliveryTime = df[i]['DeliveryDateTime']
            qty = df[i]['Demand']
            pickupDuration = df[i]['PickupDuration']
            deliveryDuration = df[i]['DeliveryDuration']
            requests.append([id, fromPoint, toPoint, qty, int(pickupDuration), int(deliveryDuration),
                             int(self.util.DateTime2Int(pickTime)), int(self.util.DateTime2Int(deliveryTime)),
                             fHub_origin, tHub_origin])

        return hubName2hubID, hubID2name, T, D, trucks, requests

    def InputExcel(self, filename):
        # read hubs
        df = pd.read_excel(open(filename, 'rb'), sheet_name='Hub')
        hubID2name = {}
        hubName2hubID = {}
        for i in df.index:
            # print(df['HubID'][i], df['Name'][i])
            h = df['HubID'][i]
            hubName2hubID[h] = i
            hubID2name[i] = h

        df = pd.read_excel(open(filename, 'rb'), sheet_name='DistanceTime')
        n = len(hubName2hubID)

        # read distance
        T = [[0 for i in range(n)] for j in range(n)]
        D = [[0 for i in range(n)] for j in range(n)]
        for k in df.index:
            fromHub = self.util.removeSubTitle(df['FromHub'][k])
            i = hubName2hubID[fromHub]
            toHub = self.util.removeSubTitle(df['ToHub'][k])
            j = hubName2hubID[toHub]
            t = df['TravelTime (s)'][k]
            d = df['Distance(m)'][k]
            # print(k, ': fromHub = ', fromHub, 'toHub = ', toHub, ' d(', i, ',', j, ') = ', d)
            T[i][j] = t
            D[i][j] = d

        # read trucks
        df = pd.read_excel(open(filename, 'rb'), sheet_name='truck')
        trucks = []
        truckID2forbidenPoints = {}
        for i in df.index:
            truckPlate = df['truckID'][i]
            cap = df['Capacity'][i]
            stWorkingTime = df['StartWorkingTime'][i]
            endWorkingTime = df['EndWorkingTime'][i]
            originLoc = df['Location'][i]
            stLocation = hubName2hubID[self.util.removeSubTitle(originLoc)]
            forbidenPoints = []
            if pd.isna(df['ForbidenPoint'][i]) == False:
                s = str(df['ForbidenPoint'][i]).split(',')
                for j in range(len(s)):
                    h = s[j].strip()
                    h = self.util.removeSubTitle(h)
                    forbidenPoints.append(hubName2hubID[h])
            truckID2forbidenPoints[i] = forbidenPoints
            maxStopPoints = df['MaxStopPoints'][i]
            trucks.append([i, truckPlate, stLocation, int(self.util.DateTime2Int(stWorkingTime)),
                           int(self.util.DateTime2Int(endWorkingTime)), cap, forbidenPoints, maxStopPoints, originLoc])

        # read requests
        df = pd.read_excel(open(filename, 'rb'), sheet_name='request')
        requests = []

        for i in df.index:
            id = df['RequestID'][i]
            fHub_origin = df['PickupPoint'][i]
            tHub_origin = df['DeliveryPoint'][i]
            fHub = self.util.removeSubTitle(fHub_origin)
            tHub = self.util.removeSubTitle(tHub_origin)
            #lao cai, son la bo qua
            if ("caugiay" in str(fHub) and ("sonla" in str(tHub) or "laocai" in str(tHub))) \
                or ("sonla" in str(fHub) or "laocai" in str(fHub)):
                continue
            if "sonla" in str(tHub) or "laocai" in str(tHub):
                tHub = "hub-caugiay"
            fromPoint = hubName2hubID[fHub]
            toPoint = hubName2hubID[tHub]
            pickTime = df['PickupDateTime'][i]
            deliveryTime = df['DeliveryDateTime'][i]
            qty = df['Demand'][i]
            pickupDuration = df['PickupDuration'][i]
            deliveryDuration = df['DeliveryDuration'][i]
            requests.append([id, fromPoint, toPoint, qty, int(pickupDuration), int(deliveryDuration),
                             int(self.util.DateTime2Int(pickTime)), int(self.util.DateTime2Int(deliveryTime)), fHub_origin, tHub_origin])

        return hubName2hubID, hubID2name, T, D, trucks, requests

    def print2excel(self, route_lst, nbServedReqs, nbUsedTrucks, totalTravelDistance, totalCapacity, pointID2hubID, pointID2hubName, hubID2name, pointID2reqID, pointID2load, outputFilename):
        solution_detail = []
        solution_summary = []
        total_weight = 0 # tong trong luong hang cho dc tren toan bo cac route
        total_cap = 0 #tổng capacity của các xe sử dụng
        solution_loadrate = [] #tỉ lệ tải của các route/km
        for route in route_lst:
            route_len = len(route.pointID_lst)
            if route_len == 2:
                continue
            load_rate_route = 0 #ti le tai tren ca route
            min_rate_segment = 100
            max_rate_segment = 0
            cur_hubName = ""
            truck_id = route.plate
            total_cap = total_cap + route.capacity

            for i in range(route_len):
                pointID = route.pointID_lst[i]
                hubName = pointID2hubName[pointID]
                weight = pointID2load[pointID]

                row = []
                row.append(truck_id)
                row.append(route.acm_hub[i])

                row.append(hubName)

                act = 'END'
                if weight > 0:
                    act = 'PICKUP'
                    total_weight = total_weight + weight
                elif weight < 0:
                    act = 'DROPOFF'
                else:
                    if i == 0:
                        act = 'START'
                row.append(act)
                row.append(pointID2reqID[pointID])
                row.append(weight)
                load_rate_segment = 0 #tỉ lệ tải trên từng chặng

                if hubName != cur_hubName: #đi đến hub mới
                    cur_hubName = hubName
                    for k in range(i, route_len):
                        if pointID2hubName[route.pointID_lst[k]] != cur_hubName:
                            load_rate_segment = route.acm_load[k - 1] * 100 / route.capacity
                            if load_rate_segment < 0.001:
                                load_rate_segment = 0
                            if load_rate_segment < min_rate_segment and load_rate_segment > 0:
                                min_rate_segment = load_rate_segment
                            if load_rate_segment > max_rate_segment:
                                max_rate_segment = load_rate_segment
                            load_rate_route = load_rate_route + load_rate_segment * (
                                        route.acm_dist[k] - route.acm_dist[i]) / 1000
                            break


                row.append(load_rate_segment)

                row.append(datetime.datetime.fromtimestamp(route.acm_time[i]))

                solution_detail.append(row)
            load_rate_route = load_rate_route * 1000 / route.acm_dist[route_len - 1]
            solution_loadrate.append([truck_id, round(load_rate_route, 2), round(min_rate_segment, 2), round(max_rate_segment, 2)])
        # sortDone = 0
        # while sortDone == 0:
        #     isSorted = 0
        #     for i in range(len(solution_detail)):
        #         for j in range(i, len(solution_detail)):
        #             row1 = solution_detail[i]
        #             row2 = solution_detail[j]
        #             if row1[0] == row2[0] and row1[1] == row2[1] and row1[2] == row2[2]:
        #                 if row1[3] == 'PICKUP' and row2[3] == 'DROPOFF':
        #                     temp = row1.copy()
        #                     solution_detail[i] = row2.copy()
        #                     solution_detail[j] = temp.copy()
        #                     isSorted = 1
        #                     break;
        #             else:
        #                 break
        #     if isSorted == 0:
        #         sortDone = 1

        solution_summary.append([nbServedReqs, nbUsedTrucks, totalCapacity, total_weight*100/(nbUsedTrucks*total_cap), totalTravelDistance, total_weight*100/(totalTravelDistance*total_cap)])
        with pd.ExcelWriter(outputFilename) as writer:
            solution_detail = pd.DataFrame(solution_detail, columns=['truck', 'seq', 'hubID', 'action', 'reqID', 'qty', 'load_rate', 'arrTime'])
            solution_detail.to_excel(writer, sheet_name='trip')
            solution_summary = pd.DataFrame(solution_summary,
                                           columns=['nbServedReqs', 'nbUsedTrucks', 'totalCapacity', 'avg_load_per_truck', 'totalTravelDistance', 'avg_load_per_km'])
            solution_summary.to_excel(writer, index = False, sheet_name='solution_summary')
            solution_loadrate = pd.DataFrame(solution_loadrate,
                                            columns=['truck_id', 'load_rate_per_km', 'min_load_ratr', 'max_load_rate'])
            solution_loadrate.to_excel(writer, index=False, sheet_name='solution_load_rate')
           # df2.to_excel(writer, sheet_name='sheet2')



