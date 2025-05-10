import buildings
import shapely
import traci
import random
import BuildingObj

class event(object):
    def __init__(self, building: BuildingObj, startTime, endTime, place_name, amenityValue):
        '''
        :param buildingID: osmid of the target building where the event happens
        :param startTime: start time of the event during the simulation
        :param endTime: end time of the event during the simulation
        :param place_name: string of current place, e.g. 'Manhattan, New York, USA'
        :param amenityValue: amenity of the target building, e.g. school, cinema
        '''
        self.buildingID = building.osmid
        self.startTime = startTime
        self.endTime = endTime
        self.geoInfo = building.geometry
        self.eventState = 0

    def getEventLocation(self):
        '''
        get the location of the event, which is also the location of the target buliding
        :return: coordinates of the event/building
        '''
        lon = 0
        lat = 0
        if isinstance(self.geoInfo, shapely.geometry.Point) == True:
            lon = self.geoInfo.x
            lat = self.geoInfo.y
        elif isinstance(self.geoInfo, shapely.geometry.Polygon) == True:
            coord = buildings.getPolygonCentr(self.geoInfo)
            lon = coord.x
            lat = coord.y
        return (lon, lat)

    def getEventState(self, timestep):
        '''
        check the state of the event, start or end
        :param timestep: time step in the simulation
        :return: eventState
        '''
        if self.startTime <= timestep <= self.endTime:
            self.eventState = 1
        else:
            self.eventState = 0
        return self.eventState

    def eventAction(self, buildingObj: BuildingObj, attriValue: int):
        buildingObj.setBuildingEnergyRate(attriValue)
        return


class Accident(event):
    accidentList = []
    def __init__(self, coordinate: tuple, facilityType: str, facilityID: str):
        self.coordinate = coordinate
        self.lon = self.coordinate[0]
        self.lat = self.coordinate[1]
        self.startTime = traci.simulation.getTime()
        self.endTime = self.startTime + random.randint(100, 150)
        self.eventState = 1
        self.facilityType = facilityType
        self.facilityID = facilityID
        Accident.accidentList.append(self)

    def getEventLocation(self):
        return self.coordinate

    def getAccidentAttr(self):
        attribute = {'coordinate': self.coordinate, 'startTime': self.startTime, 'endTime': self.endTime, 'facilityType': self.facilityType, 'facilityID': self.facilityID}
        return attribute

