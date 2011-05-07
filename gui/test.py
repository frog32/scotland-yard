def load_stations():
        station_file = open('stations.txt','r')
        station_list = station_file.readlines()
        station_file.close()

class station(object):
        def __init__(self,x,y):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x1 + 20
            self.y2 = y1 + 20
