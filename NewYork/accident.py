import numpy
import trafficLights
import event
import traci
import random

def trafficAccidentMonitor():
    '''
    generate accidents with predefined probability and return corresponding results
    :return: if a new accident is generated, return the accident object, else return 0
    '''
    accidProb = numpy.array([0.1, 0.9])
    ifAccident = numpy.random.choice([1, 0], p=accidProb.ravel())

    if ifAccident == 0:
        print('No new accidents at timestep {timestep}.'.format(timestep=traci.simulation.getTime()))
        return 0
    elif ifAccident == 1:
        trafficLightsList = trafficLights.getAllTlID()
        randomTlID = random.sample(trafficLightsList, 1)[0]
        randomTlCoord = traci.junction.getPosition(randomTlID)
        print('A new accident occurs at {coord} at timestep {timestep}, impacting traffic light {TlID}'.format(coord=randomTlCoord, timestep=traci.simulation.getTime(), TlID=randomTlID))
        newAccident = event.Accident(randomTlCoord, 'trafficLight', randomTlID)
        print(newAccident)
        print(newAccident.accidentList)
        return newAccident


