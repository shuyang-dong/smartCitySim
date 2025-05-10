import traci
import os
import sys
import dataGenerate

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:
     sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "D:/SUMO 1.5.0/bin/sumo.exe" # sumo-gui.exe for starting GUI
# sumoCmd = [sumoBinary, "-c", "SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\\NewYork.sumocfg","--queue-output", "SUMODataOutput\\queue.xml","--quit-on-end"]

if __name__ == '__main__':

    weeks = ['Week1', 'Week2']
    pathStr = 'SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\\'
    # set config file path
    configPath = pathStr + 'NewYork.sumocfg'
    # set additional file path
    additionalFilePath = pathStr + 'NewYork.poly.xml'
    # set trip file path
    #week = 'Week1'
    weekNum = 2
    tripfilesFolder = pathStr + 'TripFiles\Week{weeknum}\\'.format(weeknum=weekNum)

    tripfileNameList = os.listdir(tripfilesFolder)
    #tripfilelis = [tripfileNameList[4]]
    #print(tripfilelis)
    tripfilePath = ''
    outputFilePath = ''
    frequency = 60
    for tripfile in tripfileNameList:
        tripfilePath = tripfilesFolder + tripfile
        # set output file path
        print(tripfile)
        dayNum = tripfile[-11]
        print(dayNum)
        outputFolderPath = pathStr + 'SUMODataOutput\\2week-freq60\Week{weeknum}\\'.format(weeknum=weekNum)
        folder = os.path.exists(outputFolderPath)
        if not folder:  
            os.makedirs(outputFolderPath)  

        outputFilePath = outputFolderPath + 'Day{daynum}'.format(weeknum=weekNum,daynum=dayNum)
        folder = os.path.exists(outputFilePath)
        if not folder:  
            os.makedirs(outputFilePath)  

        dataGenerate.sumoconfigGenerate(configPath, tripfilePath, additionalFilePath, outputFilePath, frequency)
        sumoCmd = [sumoBinary, "-c", configPath, "--quit-on-end"]
        dataGenerate.simWithoutUncertain(sumoBinary, configPath, tripfilePath, additionalFilePath, outputFilePath,
                                         frequency)
