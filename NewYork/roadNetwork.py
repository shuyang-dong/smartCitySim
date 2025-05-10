import sumolib
import traci

# get all junctions' ID in the scenario
def getAllJunctID():
    junctIDList = traci.junction.getIDList()
    return junctIDList

# get info of a junction by its ID
def getJunctInfo(junID):
    '''
    parameters can be found on https://sumo.dlr.de/docs/TraCI/Junction_Value_Retrieval.html
    '''
    junInfoDict = {}
    junInfoDict['junID'] = junID
    junInfoDict['position'] = traci.junction.getPosition(junID)

    return junInfoDict


# locate nearby edges in a square with the size specified as 'radius' (half the size of the square). centered on the geo-coordinate of POI
def locateNearEdge(netStrg, lon, lat, radius):
    '''
    locate nearby edges of the target point, within certain radius
    :param netStrg: string of the net file, e.g. 'osm.net.xml'
    :param lon: lon coord of the given point
    :param lat: lat coord of the given point
    :param radius: given radius
    :return: edges within the range
    '''
    net = sumolib.net.readNet(netStrg)
    # lon, lat coordinates convert to x, y in SUMO net
    x, y = net.convertLonLat2XY(lon, lat)
    nearEdges = net.getNeighboringEdges(x, y, radius)

    return nearEdges

# locate nearby junctions of target point within given radius
def locateNearJunctions(netStrg, lon, lat, radius):
    '''
    locate nearby junctions of the target point, within certain radius
    :param netStrg: string of the net file, e.g. 'osm.net.xml'
    :param lon: lon coord of the given point
    :param lat: lat coord of the given point
    :param radius: given radius
    :return: a list of junctions within the range
    '''
    net = sumolib.net.readNet(netStrg)
    x, y = net.convertLonLat2XY(lon, lat)
    junIDList = getAllJunctID()
    junInfoList = []
    for junID in junIDList:
        junX, junY = getJunctInfo(junID)['position'][0], getJunctInfo(junID)['position'][1]
        if x-radius <= junX <= x+radius and y-radius <= junY <= y+radius:
            junInfoList.append(getJunctInfo(junID))
        else:
            continue

    return junInfoList