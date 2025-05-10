
import BuildingObj

def getEnergyRate(buildingObj:BuildingObj):
    '''
    get energy consumption rate of a building with its osmid
    :param buildingID: osmid of the target building
    :param placeName: string of current place, e.g. 'Manhattan, New York, USA'
    :param buildingAmenity: amenity of the building
    :return: energy consumption rate of the building
    '''
    buildingEnergyRate = buildingObj.energyRate

    return buildingEnergyRate
