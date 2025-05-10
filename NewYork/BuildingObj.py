class BuildingObj(object):
    def __init__(self, amenity, osmid, name, geometry, energyRate):
        self.amenity = amenity
        self.osmid = str(osmid)
        self.name = name
        self.geometry = geometry
        self.energyRate = energyRate


    def getBuildingAttributes(self):
        '''
        return attributes of a certain building
        :return:
        '''
        attribute = {'amenity': self.amenity, 'osmid': self.osmid, 'name': self.name, 'geometry': self.geometry, 'energyRate': self.energyRate}
        return attribute

    def setBuildingEnergyRate(self, energyRate):
        self.energyRate = energyRate
        return
