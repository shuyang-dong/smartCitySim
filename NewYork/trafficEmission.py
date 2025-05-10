import traci
import uncertainData


# get vehicle emission on near edges around a target coordination within radius X in last time step
def getVehicleEmissionsNearEdge(nearEdges):
    '''
    get vehicle emission on near edges around a target coordination within radius X, return a dict of emissions
    :param nearEdges: near edges returned by roadNetwork.locateNearEdge()
    :return: dict of emissions in the last time step
    '''
    CO2, CO, HC, PMx, NOx = 0, 0, 0, 0, 0
    for edge in nearEdges:
        edgID = edge[0].getID()
        CO2 += traci.edge.getCO2Emission(edgID)
        CO += traci.edge.getCOEmission(edgID)
        HC += traci.edge.getHCEmission(edgID)
        PMx += traci.edge.getPMxEmission(edgID)
        NOx += traci.edge.getNOxEmission(edgID)
    vehicleEmissions = {'CO2': uncertainData.uncertain(CO2,0.1,0.1), 'CO': uncertainData.uncertain(CO,0.1,0.1), 'HC': uncertainData.uncertain(HC,0.1,0.1), 'PMx': uncertainData.uncertain(PMx,0.1,0.1), 'NOx': uncertainData.uncertain(NOx,0.1,0.1)}

    return vehicleEmissions