import os
import sys
import csv
import pandas
import shapely
import traci
import roadNetwork
import trafficLights
import buildings
import trafficEmission
import event
import energy
import BuildingObj
import accident
import uncertainData
import dataGenerate

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "D:/SUMO 1.5.0/bin/sumo.exe" # sumo-gui.exe for starting GUI
sumoCmd = [sumoBinary, "-c", "SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\\NewYork.sumocfg","--queue-output", "SUMODataOutput\\queue.xml","--quit-on-end"]

# show all columns
pandas.set_option('display.max_columns', None)
# show all rows
pandas.set_option('display.max_rows', None)
# set display width
pandas.set_option('max_colwidth',500)



if __name__ == "__main__":

    # Manhattan, New York, USA
    place_name = 'Manhattan, New York, USA'
    netStrg = 'NewYork.net.xml'

    '''# get all juncctions in the scenario
    allJuncts = roadNetwork.getAllJunctID()
    print('All junction IDs in the scenario: ','\t', allJuncts)
    # get the info of the first junct in the list
    junction1 = roadNetwork.getJunctInfo(258965973)
    print('Info of junction 258965973', junction1)'''

    '''# start traci
    traci.start(sumoCmd)
    edgeList = traci.edge.getIDList()
    dataGenerate.fileGenerate(edgeList)
    while traci.simulation.getMinExpectedNumber() > 0:
        time = traci.simulation.getTime()
        print(time)
        if time%30 == 0:
            dataGenerate.writeFile(edgeList)
        traci.simulationStep()
    traci.close()'''

    # start traci
    traci.start(sumoCmd)
    while traci.simulation.getTime() <= 3600:
        time = traci.simulation.getTime()
        print(time)
        traci.simulationStep()
    traci.close()

    '''# Case 1
    # get all buildings of cinemas in Chicago
    amenityValue1 = 'cinema'
    energyRate = 20.0
    # initialize the cinema objects in the scenario
    cinemaObjsList = buildings.initizlizeBuildingObj(place_name, amenityValue1, energyRate)
    print('All cinemas in the scenario: ', '\n', cinemaObjsList)
    # get the information of one cinema in the list
    targetCinema = cinemaObjsList[5]
    print('Target cinema:', '\n', targetCinema.getBuildingAttributes())
    # get the coordinate of the cinema
    coord = targetCinema.geometry
    print('Coordinate of the target cinema: ', coord)
    # search for the intersections around the target cinema within a square area set 1000m around the coord in each direction
    nearbyIntersection = roadNetwork.locateNearJunctions(netStrg, coord.x, coord.y, 100)
    print('Intersections around the target cinema: ', '\n', nearbyIntersection)'''

    '''# Case 2
    accidentList = []
    flag = True
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # generate accidents with given probability at some particular time steps in the simulation
        if traci.simulation.getTime() % 10 == 0:
            potentialAccident = accident.trafficAccidentMonitor()
            if potentialAccident != 0:
                accidentList.append(potentialAccident)

        if accidentList != []:
            # choose the first accident happens in the scenario and adjust the traffic light it impacts
            targetAccident = accidentList[0]
            while(flag):
                print('Information of target accident: ', '\n', targetAccident.getAccidentAttr())
                flag = False
            targetTlID = targetAccident.facilityID
            targetTlCoord = roadNetwork.getJunctInfo(targetTlID)['position']
            nearEdges = roadNetwork.locateNearEdge(netStrg, targetTlCoord[0], targetTlCoord[1], 300)
            # switch phases for traffic light according to the emissions around
            trafficLights.phaseAdjustEmission(netStrg, targetTlID, 200)
            print('Timestep: ', traci.simulation.getTime(),'   Current phase: ', traci.trafficlight.getPhase(targetTlID),
            '   Current phase duration: ',traci.trafficlight.getPhaseDuration(targetTlID))
    traci.close()'''


    '''# Case 3
    # initialize the school objects in the scenario
    amenityValue1 = 'cinema'
    energyRate = 20.0
    cinemaObjsList = buildings.initizlizeBuildingObj(place_name, amenityValue1, energyRate)
    # get the information of one cinema in the list
    targetCinema = cinemaObjsList[5]
    print('Target cinema:', '\n', targetCinema.getBuildingAttributes())
    # set an event to the target cinema, start time = 10, end time = 15
    repairEvent = event.event(targetCinema, 5, 10, place_name, amenityValue1)
    # start traci
    traci.start(sumoCmd)
    # check the state of the event and change the energy consumption rate when the event is finished
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print('Timestep: ', traci.simulation.getTime(), '   State of the repairing event: ', repairEvent.getEventState(traci.simulation.getTime()),
              '   Energy consumption rate: ', targetCinema.energyRate)
        if traci.simulation.getTime() == repairEvent.startTime:
            print('Repair begins.')
        elif repairEvent.startTime < traci.simulation.getTime() < repairEvent.endTime:
            print('Repair ongoing.')
        elif traci.simulation.getTime() == repairEvent.endTime:
            repairEvent.eventAction(targetCinema, 30)
            print('Repair finished.')
    traci.close()'''



    '''# change the tl phase according to the event state
                time = traci.simulation.getTime()  # current time step in the simulation
                print('current time: ', time, ' current event state: ', schoolEvent.getEventState(time))
                if schoolEvent.getEventState(
                        time) == 1:  # if the event has began, change the phase of the traffic light and print
                    trafficLights.simplePhaseAdjust(tl0ID)
                    print('current phase of tl0: ', traci.trafficlight.getPhase(tl0ID))'''

    '''#
    # get energy consumption rate of a school with given osmid
    schoolID0 = '711552605'
    for school in schoolObjsList:
        if school.osmid == schoolID0:
            school.setBuildingEnergyRate(30)
            schoolEnergyRate = energy.getEnergyRate(school)
            print('Energy consumption rate of school 711552605 is: ', schoolEnergyRate)



    # get schools that geometry = Point
    pointSchools = buildings.getBuildingswithType(schoolObjsList, shapely.geometry.Point)
    print(pointSchools)
    # get info of the first school
    
    # get libraries near pointSchools[0]
    nearbyLibrary = buildings.locateNearBuildingsofPoint(pointSchools[0], 'library', 1000)
    print('Libraries near pointSchool {schoolID}: '.format(schoolID=pointSchools[0]), nearbyLibrary)
    # get schools that geometry = Polygon
    polygonSchools = buildings.getBuildingswithType(schoolObjsList, shapely.geometry.Polygon)
    # first polygon school in the list
    polySchoolGeo = polygonSchools[0]['geometry']
    # centroid of the first polygon school
    centroid = buildings.getPolygonCentr(polySchoolGeo)
    # print('Centroid Coords: ', centroid)
    # get libraries near polygonSchools[0]
    nearbyLibrary = buildings.locateNearBuildingsofPolygon(polygonSchools[0], 'library', 3000)
    print('Libraries near polygonSchool {schoolID}: '.format(schoolID=polygonSchools[0]), nearbyLibrary)

    # set an event at a specific school
    targetPoint = (-87.63, 41.88)
    nearbySchools = buildings.locateNearBuildingsofCoord(targetPoint[0], targetPoint[1], 'school', 1000) # get schools near target point,radius=300
    amenityValue1 = 'school'
    school0 = nearbySchools[0]  # the first school in the list
    school0ID = school0['osmid']  # the osmid of the first school
    school0Info = buildings.getBuildingbyID(school0ID, place_name, amenityValue1)  # info of the first school: osmid, name, geometry
    print(school0ID, school0Info)
    schoolEvent = event.event(school0ID, 200, 400, place_name, amenityValue1)  # a event happens at school0
    eventLocation = schoolEvent.getEventLocation()  # location of the event/school0
    elon, elat = eventLocation[0], eventLocation[1]

    # start traci
    traci.start(sumoCmd)
    nearTls = trafficLights.locateNearTls(netStrg, elon, elat, 300)  # get nearby traffic lights of the event location
    print(nearTls)
    tl0ID = nearTls[0]['tlID']  # ID of the first tl in the list

    # get all junctions' ID in the scenario
    alljunctID = roadNetwork.getAllJunctID()

    # get info of all junctions in the scenario
    for junID in alljunctID:
        print(roadNetwork.getJunctInfo(junID))

    # get all traffic lights' ID in the scenario
    tlIDList = trafficLights.getAllTlID()
    tlID0 = tlIDList[0]
    print(tlID0)
    
    # get a dictionary of all tls and their programs, key = traffic light ID, value = traffic light logics
    allTlProgramDict = trafficLights.getAllTlProgLogic()

    # get tl info of each traffic light by tlID
    for tlID in tlIDList:
        print(tlID)
        print(trafficLights.getTlInfo(tlID)['phases'])

    # get nearby edges
    nearEdges = roadNetwork.locateNearEdge(netStrg, -87.63, 41.88, radius=100)

    accidentList = []

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # generate accidents with given probability at particular time in the simulation
        if traci.simulation.getTime()%10 == 0:
            potentialAccident = accident.trafficAccidentMonitor()
            if potentialAccident != 0:
                accidentList.append(potentialAccident)
        # get vehicle emissions per time step on near edges
        vehicleEmissions = trafficEmission.getVehicleEmissionsNearEdge(nearEdges)
        print('step: ', traci.simulation.getTime(), "emissions: ", vehicleEmissions)
        # switch phases for traffic light according to the emissions around
        trafficLights.phaseAdjustEmission(netStrg,'102708200', 200)
        print(traci.trafficlight.getPhase('102708200'), traci.trafficlight.getPhaseDuration('102708200'))

        # change the tl phase according to the event state
        time = traci.simulation.getTime()  # current time step in the simulation
        print('current time: ',time, ' current event state: ',schoolEvent.getEventState(time))
        if schoolEvent.getEventState(time) == 1:  # if the event has began, change the phase of the traffic light and print
            trafficLights.simplePhaseAdjust(tl0ID)
            print('current phase of tl0: ', traci.trafficlight.getPhase(tl0ID))


    traci.close()

    print(accidentList)
'''

