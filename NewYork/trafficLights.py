import traci
import sumolib
import trafficEmission
import roadNetwork

# get all tls ID in the scenario
def getAllTlID():
    trafficLightsIDList = list(traci.trafficlight.getIDList())
    return trafficLightsIDList

# get traffic light program for all traffic lights in the scenario, return a dictionary
def getAllTlProgLogic():
    tlIDList = traci.trafficlight.getIDList()
    tlProgramDict = {}
    for tlID in tlIDList:
        tlProgramDict[tlID] = traci.trafficlight.getAllProgramLogics(tlID)
    return tlProgramDict

# get info of a traffic light with its ID
def getTlInfo(tlID):
    '''
    more parameters can be found on https://sumo.dlr.de/pydoc/traci._trafficlight.html#TrafficLightDomain-getIDList
    '''
    tlInfoDict = {}
    tlLogic = traci.trafficlight.getAllProgramLogics(tlID)[0]
    tlInfoDict['logic'] = tlLogic
    tlInfoDict['phases'] = tlLogic.getPhases()
    tlInfoDict['subID'] = tlLogic.getSubID()
    tlInfoDict['type'] = tlLogic.getType()
    return tlInfoDict

# locate nearby traffic lights of target point within given radius
def locateNearTls(netStrg, lon, lat, radius):
    '''
    locate nearby traffic lights of the target point, within certain radius
    :param netStrg: string of the net file, e.g. 'osm.net.xml'
    :param lon: lon coord of the given point
    :param lat: lat coord of the given point
    :param radius: given radius
    :return: a list of traffic lights info, within the range
    '''
    nearJun = roadNetwork.locateNearJunctions(netStrg, lon, lat, radius)
    allTlID = getAllTlID()
    nearTlList = []
    for jun in nearJun:
        if jun['junID'] in allTlID:
            tlDict = {'tlID': jun['junID'], 'position':jun['position']}
            nearTlList.append(tlDict)
        else:
            continue
    return nearTlList

# change the state of traffic light according  to the vehicle emissions
def phaseAdjustEmission(netStrg, tlID, radius):
    '''
    switch the phases according to the vehicle emissions around the junction
    :param tlID: traffic light ID = junction ID
    :param radius: range of area for calculating emissions
    :return:
    '''
    net = sumolib.net.readNet(netStrg)
    currentPhase = traci.trafficlight.getPhase(tlID)
    junCoord = roadNetwork.getJunctInfo(tlID)['position']
    x, y = junCoord[0], junCoord[1]
    # x to lon, y to lat
    lon, lat = net.convertXY2LonLat(x, y)
    nearEdges = roadNetwork.locateNearEdge(netStrg, lon, lat, radius)
    emissionsAround = trafficEmission.getVehicleEmissionsNearEdge(nearEdges)
    print('Surrounding CO2 emissions: ', emissionsAround['CO2'])
    if emissionsAround['CO2'] > 500 and currentPhase < len(getTlInfo(tlID)['phases'])-1:
        traci.trafficlight.setPhase(tlID, currentPhase+1)
    elif emissionsAround['CO2'] > 500 and currentPhase == len(getTlInfo(tlID)['phases'])-1:
        traci.trafficlight.setPhase(tlID, 0)
    elif emissionsAround['CO2'] <= 500:
        traci.trafficlight.setPhase(tlID, currentPhase)

    return

# simple phase adjustment for testing
def simplePhaseAdjust(tlID):
    currentPhase = traci.trafficlight.getPhase(tlID)
    if currentPhase < len(getTlInfo(tlID)['phases'])-1:
        traci.trafficlight.setPhase(tlID, currentPhase+1)
    else:
        traci.trafficlight.setPhase(tlID, 0)
    return