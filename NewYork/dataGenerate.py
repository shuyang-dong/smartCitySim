import os
import sys
import csv
import traci
import numpy
import xlrd
from xml.etree.ElementTree import ElementTree,Element
import lxml.etree as ET


# edge id list edgeList
# generate output files
def fileGenerate(edgeList: list):
    index = 1
    for id in edgeList:
        path = "D:\\ShuyangDongDocument\\UVA\\UVA-Research\\SmartCitySimulation\\SUMOSimulation\\SmartCitySUMOSim\\NewYork\\DataOutput\\"+str(index)+".csv"
        with open(path, 'w', newline='') as f:
            csv_head = ["edgeID", "timeStep", "CO2", "CO", "HC", "NOx", "PMx", "Noise", "lastStepHaltingNum", "lastStepMeanSpeed"]
            csv_write = csv.DictWriter(f, fieldnames=csv_head)
            csv_write.writeheader()
        index += 1
    return

# write data to the files
def writeFile(edgeList: list):
    index = 1
    for id in edgeList:
        path = "D:\\ShuyangDongDocument\\UVA\\UVA-Research\\SmartCitySimulation\\SUMOSimulation\\SmartCitySUMOSim\\NewYork\\DataOutput\\" + str(
            index) + ".csv"
        with open(path, 'a+', newline='') as f:
            csv_head = ["edgeID", "timeStep", "CO2", "CO", "HC", "NOx", "PMx", "Noise", "lastStepHaltingNum",
                        "lastStepMeanSpeed"]
            csv_write = csv.DictWriter(f, fieldnames=csv_head)
            CO2 = traci.edge.getCO2Emission(id)
            CO = traci.edge.getCOEmission(id)
            HC = traci.edge.getHCEmission(id)
            NOx = traci.edge.getNOxEmission(id)
            PMx = traci.edge.getPMxEmission(id)
            Noise = traci.edge.getNoiseEmission(id)
            haltNum = traci.edge.getLastStepHaltingNumber(id)
            meanSpeed = traci.edge.getLastStepMeanSpeed(id)
            dataRow = {"edgeID": id, "timeStep": traci.simulation.getTime(), "CO2": CO2, "CO": CO, "HC": HC,
                       "NOx": NOx, "PMx": PMx, "Noise": Noise, "lastStepHaltingNum": haltNum,
                       "lastStepMeanSpeed": meanSpeed}
            csv_write.writerow(dataRow)

        index += 1
        '''#
        if index <= 100:
            path = "D:\\ShuyangDongDocument\\UVA\\UVA-Research\\SmartCitySimulation\\SUMOSimulation\\SmartCitySUMOSim\\NewYork\\DataOutput\\" + str(
                index) + ".csv"
            with open(path, 'a+', newline='') as f:
                csv_head = ["edgeID", "timeStep", "CO2", "CO", "HC", "NOx", "PMx", "Noise", "lastStepHaltingNum",
                            "lastStepMeanSpeed"]
                csv_write = csv.DictWriter(f, fieldnames=csv_head)
                CO2 = traci.edge.getCO2Emission(id)
                CO = traci.edge.getCOEmission(id)
                HC = traci.edge.getHCEmission(id)
                NOx = traci.edge.getNOxEmission(id)
                PMx = traci.edge.getPMxEmission(id)
                Noise = traci.edge.getNoiseEmission(id)
                haltNum = traci.edge.getLastStepHaltingNumber(id)
                meanSpeed = traci.edge.getLastStepMeanSpeed(id)
                dataRow = {"edgeID": id, "timeStep": traci.simulation.getTime(), "CO2": CO2, "CO": CO, "HC": HC,
                           "NOx": NOx, "PMx": PMx, "Noise": Noise, "lastStepHaltingNum": haltNum,
                           "lastStepMeanSpeed": meanSpeed}
                csv_write.writerow(dataRow)

            index += 1'''
    return

# generate sumo configuration file
def sumoconfigGenerate(configFile:str, tripFilename: str, additionalFile: str, outputpath: str, freq: int):

    # change sumoconfig route file path
    configPath = configFile
    # read sumoconfig file
    tree = ET.parse(configPath)
    # find node for route-files and change the attribute value
    path = 'input/route-files'
    node = tree.find(path)
    node.set('value', tripFilename)
    # write into the file
    tree.write(configPath, encoding="utf-8", xml_declaration=True)

    # change output file path in additional file
    # read additional file
    # tree = ElementTree()
    tree = ET.parse(additionalFile)
    # find node for output files and change the attribute value
    path = 'edgeData'
    nodes = tree.findall(path)
    #print(nodes)
    filename = ''
    for node in nodes:
        if node.get('id') == '1':
            filename = 'edgeTraffic.xml'
        elif node.get('id') == '2':
            filename = 'edgeEmission.xml'
        elif node.get('id') == '3':
            filename = 'edgeNoise.xml'
        elif node.get('id') == '4':
            filename = 'amitranEdgeTraffic.xml'
        #print(node)
        node.set('file', outputpath+'\\'+filename)
        node.set('freq', str(freq))
    # write into the file
    tree.write(additionalFile, encoding="utf-8", xml_declaration=True)

    return

# split the total traffic volume into different flows
def flowVolumnSplit(splitNum, totalVol):
    # assume each flow has at least 5% of the total volume
    leastVeh = int(totalVol*0.05)
    restVol = totalVol - leastVeh*splitNum
    # list storing the traffic volume of splitNum random flows
    randomFlowVol = []
    # generate splitNum-1 random num and sorted
    randomNum = []
    for i in range(splitNum-1):
        num = numpy.random.randint(1, restVol)
        randomNum.append(num)
    randomNum.extend([0, restVol])
    randomNum = sorted(randomNum)
    # calculate values of random flows
    for k in range(len(randomNum)-1):
        ele = randomNum[k]
        nextEle = randomNum[k+1]
        volume = nextEle-ele + leastVeh
        randomFlowVol.append(volume)

    return randomFlowVol

# generate flow files
def flowGenerate(filename: str):
    '''
    <flow id="f2" begin="0" end="100" number="23" from="beg" to="end" via="e1 e23 e7"/>
    :return:
    '''

    # get traffic volumes
    flowCount = 1
    dayCount = 1
    beginTime = 0
    endTime = 3600
    '''#
    flowDict = {'587061858#2': ['-gneE2', '391864586#9', 'gneE33', 'gneE39', 'gneE13'],  # Madison Avenue
                '68674962#23': ['68674962#27', 'gneE39', 'gneE11', '46694760#12', '5670818#5'],  # Park Avenue SB
                '686125782#9': ['686125782#15', '5670507#5', '421853961#1', 'gneE21', 'gneE25'],  # Park Avenue NB
                '387128267#11': ['-gneE38', '579565231#6', 'gneE32', 'gneE29', '46694757#5'],  # Lexington Avenue
                '579565231#3': ['579565231#8', '5672524#5', 'gneE12', '46694762#11', 'gneE10'],  # 3rd Avenue
                '391864586#11': ['gneE39', 'gneE13', '497154281#9', '421853961#1', '46694762#6'],  # 2nd Avenue
                'gneE30': ['-gneE2', '387128267#7', '46694757#9', 'gneE34', 'gneE21'],  # 1st Avenue
                'gneE27': ['gneE25', 'gneE19', '46694757#7', '46694762#7', '541331866'],  # York Avenue NB
                '-gneE27': ['gneE34', '5672524#5', '46694757#8', '-gneE7', '-46694753#1'],  # York Avenue SB
    }'''
    outEdgeList = ['-46694753#1', '68674962#27', 'gneE34', 'gneE39', '-gneE7', 'gneE21', 'gneE23', 'gneE25', '-gneE26',
                                '-gneE2', 'gneE33', '579565231#8', '686125782#15', 'gneE10', 'gneE9', '46694762#11', '541331866', '46694760#12'] # 18
    outEdgeList = ['-46694753#1', 'gneE39', '-gneE7', 'gneE21', '-gneE26',
                   '-gneE2', 'gneE33', '579565231#8', 'gneE9', '46694762#11']  # 18
    '''#
    inEdgeList1 = ['5670818#1', '46694762#7', '-5673456#0', '-587061846#5', '-gneE19', '587061858#6', '68674962#18', 'gneE29', '387128267#9', '-497154281#10'] # 10 each
    inEdgeList2 = ['5672524#1', '5672524#4', 'gneE38', '46694762#4', 'gneE12', '686125782#12', '68674962#21', '387128267#9', '579565231#6', 'gneE29']
    inEdgeList3 = ['46694762#10', '-5673456#0', '46694760#7', '5670818#7', 'gneE14', '686125782#12', '68674962#18', '579565231#6', '391864586#9', '-gneE1']
    inEdgeList4 = ['5670507#3', '46694753#5', '5673456#3', '46694762#6', '-587061846#5', '587061858#6', '68674962#18', '387128267#9', '421853961#1', '-497154281#10']
    inEdgeList5 = ['5672524#3', '46694753#5', '5670818#4', 'gneE38', '5670818#7', 'gneE18', '68674962#21', '579565231#6', '391864586#9', '-497154281#10']
    inEdgeList6 = ['46694757#9', '5672524#4', '5670818#5', 'gneE38', '-gneE19', '68674962#18', '68674962#21', 'gneE29', '421853961#1', '-497154281#10']
    inEdgeList7 = ['46694753#5', '-46694753#1', '5672524#4', '5670818#5', 'gneE19', '587061858#6', '686125782#12', '387128267#9', 'gneE29', '-gneE1']
    inEdgeList8 = ['46694762#10', '46694762#7', '5670818#4', '46694762#6', 'gneE12', '68674962#18', '387128267#9', '391864586#9', '421853961#1', '-497154281#10']
    inEdgeList9 = ['5672524#3', '5673456#3', '46694762#6', '-5673456#4', 'gneE18', '587061858#6', '68674962#18', '579565231#6', '421853961#1', '-497154281#10']
    #'''
    '''#
    inEdgeList1 = ['-gneE2', '391864586#9', 'gneE33', 'gneE39', 'gneE13', '-gneE19', '587061858#6', '68674962#18'] # 8
    inEdgeList2 = ['68674962#27', 'gneE39', 'gneE11', '46694760#12', '5670818#5', 'gneE12', '686125782#12', '68674962#21']
    inEdgeList3 = ['686125782#15', '5670507#5', '421853961#1', 'gneE21', 'gneE25', '5670818#7', 'gneE14', '686125782#12']
    inEdgeList4 = ['-gneE38', '579565231#6', 'gneE32', 'gneE29', '46694757#5', '-587061846#5', '587061858#6', '68674962#18']
    inEdgeList5 = ['579565231#8', '5672524#5', 'gneE12', '46694762#11', 'gneE10', 'gneE38', '5670818#7', 'gneE18']
    inEdgeList6 = ['gneE39', 'gneE13', '497154281#9', '421853961#1', '46694762#6','-gneE19', '68674962#18', '68674962#21']
    inEdgeList7 = ['-gneE2', '387128267#7', '46694757#9', 'gneE34', 'gneE21', 'gneE19', '587061858#6', '686125782#12']
    inEdgeList8 = ['gneE25', 'gneE19', '46694757#7', '46694762#7', '541331866', '46694762#6', 'gneE12', '68674962#18']
    inEdgeList9 = ['gneE34', '5672524#5', '46694757#8', '-gneE7', '-46694753#1', 'gneE18', '587061858#6', '68674962#18']'''

    inEdgeList1 = ['-gneE2', '391864586#9', 'gneE33', 'gneE39', 'gneE13', '5672524#4', '46694757#7', '68674962#21', '5670507#1', '46694762#11']  # 10
    inEdgeList2 = ['68674962#27', 'gneE39', 'gneE11', '46694760#12', '5670818#5', 'gneE34', '46694760#12', '5670507#5', 'gneE38', 'gneE29']
    inEdgeList3 = ['686125782#15', '5670507#5', '421853961#1', 'gneE21', 'gneE25', '5670507#3', '5672524#4', '387128267#8', '391864586#8', '579565231#7']
    inEdgeList4 = ['-gneE38', '579565231#6', 'gneE32', 'gneE29', '46694757#5', '5670818#5', '5670507#5', '587061846#5', '5670818#7', '391864586#10']
    inEdgeList5 = ['579565231#8', '5672524#5', 'gneE12', '46694762#11', 'gneE10', '5670507#5', '5672524#7', '5673456#4', '5670507#7', '587061858#4']
    inEdgeList6 = ['gneE39', 'gneE13', '497154281#9', '421853961#1', '46694762#6', 'gneE29', '541331867', '46694760#8', '68674962#27', '5670818#7']
    inEdgeList7 = ['-gneE2', '387128267#7', '46694757#9', 'gneE34', 'gneE21', 'gneE17', '46694762#6', '-gneE26', '421853961#1', 'gneE15']
    inEdgeList8 = ['gneE25', 'gneE19', '46694757#7', '46694762#7', '541331866', 'gneE23', 'gneE33', '391864586#8', '46694762#6', '-5673456#3']
    inEdgeList9 = ['gneE34', '5672524#5', '46694757#8', '-gneE7', '-46694753#1', '46694760#7', '391864586#11', '46694760#5', 'gneE37', '-46694753#5']


    EdgeList1 = inEdgeList1
    EdgeList2 = inEdgeList2
    EdgeList3 = inEdgeList3
    EdgeList4 = inEdgeList4
    EdgeList5 = inEdgeList5
    EdgeList6 = inEdgeList6
    EdgeList7 = inEdgeList7
    EdgeList8 = inEdgeList8
    EdgeList9 = inEdgeList9

    flowDict = {'587061858#2': EdgeList1,  # Madison Avenue
                '68674962#23': EdgeList2,  # Park Avenue SB
                '686125782#9': EdgeList3,  # Park Avenue NB
                '387128267#11': EdgeList4,  # Lexington Avenue
                '579565231#3': EdgeList5,  # 3rd Avenue
                '391864586#11': EdgeList6,  # 2nd Avenue
                'gneE30': EdgeList7,  # 1st Avenue
                'gneE27': EdgeList8,  # York Avenue NB
                '-gneE27': EdgeList9,  # York Avenue SB
                }


    workbook = xlrd.open_workbook(filename)
    tablelist = ['DailyTrafficVolume-1', 'DailyTrafficVolume-2', 'DailyTrafficVolume-3', 'DailyTrafficVolume-4',
                 'DailyTrafficVolume-5', 'DailyTrafficVolume-6', 'DailyTrafficVolume-7']
    #tablelist = ['DailyTrafficVolume-5']
    for tableID in tablelist:
        with open("{NewYorkTrips}.trips.xml".format(NewYorkTrips=tableID), "w", encoding='utf-8') as f:
            str = '<routes>'
            ftext = f.write(str)
            ftext = f.write('\n')
        table = workbook.sheet_by_name(tableID)
        hourVolume = {}
        for hour in range(9,34):
            for row in range(1, table.nrows):
                edgeID = table.row_values(row)[1]  # get edgeID in the table
                volume = table.cell_value(row, hour)
                hourVolume[edgeID] = volume
            print(hourVolume)
            for edge in hourVolume.keys():
                for key in flowDict.keys():
                    if edge == key:
                        start = edge
                        endList = flowDict[key]
                        totalVol = int(hourVolume[edge]*0.7) # discount
                        flowVols = flowVolumnSplit(10, totalVol)
                        print(flowVols)
                        for i in range(len(endList)):
                            to = endList[i]
                            flowVolume = flowVols[i]
                            with open("{NewYorkTrips}.trips.xml".format(NewYorkTrips=tableID), "a+", encoding='utf-8') as f:
                                str = '<flow id="{flowID}" begin="{beginTime}" end="{endTime}" number="{flowVolume}" from="{start}" to="{to}"/>'.format(
                                    flowID=flowCount, flowVolume=int(flowVolume),beginTime=beginTime, endTime=endTime, start=start, to=to)
                                ftext = f.write(str)
                                ftext = f.write('\n')
                            flowCount += 1
            beginTime = endTime + 1
            endTime = beginTime + 3600

        with open("{NewYorkTrips}.trips.xml".format(NewYorkTrips=tableID), "a+", encoding='utf-8') as f:
            str = '</routes>'
            ftext = f.write(str)

        beginTime = 0
        endTime = 3600
        flowCount = 1

    return

# run simulation without uncertainty
def simWithoutUncertain(sumoBinary, configPath, tripfilePath, additionalFilePath, outputFilePath, frequency):

    sumoCmd = [sumoBinary, "-c", configPath, "--quit-on-end"]

    traci.start(sumoCmd)
    while traci.simulation.getMinExpectedNumber() > 0:
        print(traci.simulation.getTime())
        traci.simulationStep()
    traci.close()

    return

'''#
if __name__ == '__main__':

    file = 'D:\ShuyangDongDocument\\UVA\\UVA-Research\SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\Traffic_Volume_Counts_2019_V1.xlsx'
    flowGenerate(file)
    #
    configFile = 'D:\ShuyangDongDocument\\UVA\\UVA-Research\SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\\NewYork.sumocfg'
    Tripfile = 'DailyTrafficVolume-1.trips.xml'
    routeFile = 'D:\ShuyangDongDocument\\UVA\\UVA-Research\SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\TripFiles\Week1\{tripfile}'.format(tripfile=Tripfile)

    additionalFile = 'D:\ShuyangDongDocument\\UVA\\UVA-Research\SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\\NewYork.poly.xml'
    outputPath = 'D:\ShuyangDongDocument\\UVA\\UVA-Research\SmartCitySimulation\SUMOSimulation\SmartCitySUMOSim\\NewYork\SUMODataOutput\\2week-freq60\Week1\Day1'
    frequency = 60
    sumoconfigGenerate(configFile, routeFile, additionalFile, outputPath, frequency)'''
