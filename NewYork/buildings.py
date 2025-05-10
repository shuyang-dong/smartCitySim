import osmnx
from pandas import DataFrame
import shapely
import energy
import BuildingObj

# initialize one type of buildingObjs in the simulation
def initizlizeBuildingObj(place_name, amenity, energyRate):
    '''
    initialize one type of buildingObjs in the simulation
    :param place_name: string of target place, e.g. 'Manhattan, New York, USA'
    :param amenity: string, type of the target building e.g. school, university, ect. See: https://wiki.openstreetmap.org/wiki/Key:amenity?uselang=zh-TW
    :param energyRate: energy consumption rate for this type of buildings
    :return: all buildingObjs in the scenario
    '''
    buildObjList = []
    buildingInfo = getBuildingsbyAmen(place_name,amenity)
    for building in buildingInfo:
        buildingAmen = amenity
        buildingID = building['osmid']
        buildingName = building['name']
        buildingGeo = building['geometry']
        #BuildingObj.BuildingObj(buildingAmen, buildingID, buildingName, buildingGeo, energyRate)
        buildObjList.append(BuildingObj.BuildingObj(buildingAmen, buildingID, buildingName, buildingGeo, energyRate))
    return buildObjList


# get one kind of buildings by key:amenity in the OSM
def getBuildingsbyAmen(place_name, amenity):
    '''
    get specific type of buildings in the map of a given place by Key:amenity
    :param place_name: string of target place, e.g. 'Manhattan, New York, USA'
    :param amenity: string, type of the target building e.g. school, university, ect. See: https://wiki.openstreetmap.org/wiki/Key:amenity?uselang=zh-TW
    :param energyRate: energy consumption rate of this type of buildings
    :return: List of dictionaries of target buildings: osmid, type(point, polygon, ect) and coordinates, add others if needed.
    '''
    tags = {'amenity': amenity}
    all_pois = osmnx.pois.pois_from_place(place_name, tags, which_result=1)
    # get osmid, name and geometry values of the buildings with key: amenity
    amenityOsmID = all_pois.osmid.tolist()
    amenityName = all_pois.name.tolist()
    amenityPos = all_pois.geometry.tolist()
    amenityList = []
    for amenityID in amenityOsmID:
        index = amenityOsmID.index(amenityID)
        amenityDict = {'osmid':amenityID, 'name':amenityName[index], 'geometry':amenityPos[index]}
        amenityList.append(amenityDict)

    '''amenityInfo = DataFrame(
        { 'osmid': amenityOsmID,
          'name': amenityName,
          'geometry': amenityPos
        }
    )'''
    return amenityList

# get building coordinates by osmid
def getBuildingbyID(buildingID, place_name, amenity):
    '''
    get building coordinates by osmid
    :param buildingID: osmid of the building
    :param place_name: string of current place, e.g. 'Manhattan, New York, USA'
    :param amenity: amenity of the target building, e.g. school, cinema
    :return: dictionary of building info
    '''
    amenityList = getBuildingsbyAmen(place_name, amenity)
    for building in amenityList:
        if buildingID == building['osmid']:
            return building


# get specific kind of buildings with different geometry types (= Point, Polygon, ect.)
def getBuildingswithType(buildingObjs, buildingType):
    '''
    get specific kind of buildings with different geometry types (= Point, Polygon, ect.)
    :param buildingsInfo: DataFrame returned by fun:getBuildingsbyAmen
    :param buildingType: shapely.geometry.Point, shapely.geometry.Polygon, Point has one tuple for coordinates, Polygon has multiple coordinates to discribe its edge.
    :return: list of info of buildings, each building has a dictionary
    '''
    pointBuildingsList = []
    polygonBuildingsList = []
    for building in buildingObjs:
        attribute = building.getBuildingAttributes()
        id = attribute['osmid']
        name = attribute['name']
        geoInfo = attribute['geometry']
        if isinstance(geoInfo, shapely.geometry.Point):
            lon = geoInfo.x
            lat = geoInfo.y
            attribute['coords'] = (lon, lat)
            pointBuilding = attribute # {'osmid': id, 'name': name, 'geometry': geoInfo, 'coords': (lon, lat)}
            pointBuildingsList.append(pointBuilding)
        elif isinstance(geoInfo, shapely.geometry.Polygon):
            polygonBuilding = {'osmid': id, 'name': name, 'geometry': geoInfo}
            polygonBuildingsList.append(polygonBuilding)
    '''for i in range(0, len(buildingsInfo)):
        id = buildingsInfo.osmid[i]
        name = buildingsInfo.name[i]
        geoInfo = buildingsInfo.geometry[i]
        if isinstance(geoInfo, shapely.geometry.Point):
            lon = geoInfo.x
            lat = geoInfo.y
            pointBuilding = {'osmid': id, 'name': name, 'geometry': geoInfo, 'coords': (lon, lat)}
            pointBuildingsList.append(pointBuilding)
        elif isinstance(geoInfo, shapely.geometry.Polygon):
            polygonBuilding = {'osmid': id, 'name': name, 'geometry': geoInfo}
            polygonBuildingsList.append(polygonBuilding)'''

    # return different kinds of buildings
    if buildingType == shapely.geometry.Point:
        return pointBuildingsList
    elif buildingType == shapely.geometry.Polygon:
        return polygonBuildingsList

# locate nearby buildings of a given point within distance by target amenity
def locateNearBuildingsofCoord(lon, lat, targetAmenity, distance):
    '''
    locate nearby buildings with target amenity value of a given point's coords, within some distance N, S, E, W of the point.
    :param lon: lon of the point
    :param lat: lat of the point
    :param targetAmenity: the amenity value of target surrounding buildings
    :param distance: distance in meters, N, S, E, W of the point.
    :return: list of targetBuildings
    '''
    tags = {'amenity': targetAmenity}
    targetBuildings = osmnx.pois.pois_from_point((lat, lon), tags, dist=distance)
    amenityOsmID = targetBuildings.osmid.tolist()
    amenityName = targetBuildings.name.tolist()
    amenityPos = targetBuildings.geometry.tolist()
    targetBuildingList = []
    for amenityID in amenityOsmID:
        index = amenityOsmID.index(amenityID)
        amenityDict = {'osmid': amenityID, 'name': amenityName[index], 'geometry': amenityPos[index]}
        targetBuildingList.append(amenityDict)
    return targetBuildingList

# locate nearby buildings of a center Building (geometry = point) within distance by target amenity
def locateNearBuildingsofPoint(centerBuild, targetAmenity, distance):
    '''
    locate nearby buildings with target amenity value of a given Point building, within some distance N, S, E, W of the point.
    :param centerBuild: the given building, dictionary element in the returned list of fun: getBuildingswithType
    :param targetAmenity: the amenity value of target surrounding buildings
    :param distance: distance in meters, N, S, E, W of the point.
    :return: list of targetBuildings
    '''
    geometry = centerBuild['geometry']
    lon = geometry.x
    lat = geometry.y
    tags = {'amenity':targetAmenity}
    targetBuildings = osmnx.pois.pois_from_point((lat, lon), tags, dist=distance)
    amenityOsmID = targetBuildings.osmid.tolist()
    amenityName = targetBuildings.name.tolist()
    amenityPos = targetBuildings.geometry.tolist()
    targetBuildingList = []
    for amenityID in amenityOsmID:
        index = amenityOsmID.index(amenityID)
        amenityDict = {'osmid': amenityID, 'name': amenityName[index], 'geometry': amenityPos[index]}
        targetBuildingList.append(amenityDict)

    return targetBuildingList

# get centroid of polygon
def getPolygonCentr(polygon: shapely.geometry.Polygon):
    '''
    get the coordinates of centroid of a polygon, source: https://shapely.readthedocs.io/en/latest/manual.html
    :param polygon: building with type: shapely.geometry.Polygon
    :return: coords of the centroid, type: shapely.geometry.Point
    '''
    centroid = shapely.wkt.loads(polygon.centroid.wkt)

    return centroid

# locate nearby buildings of a center Building (geometry = polygon) within distance by target amenity
def locateNearBuildingsofPolygon(centerBuild, targetAmenity, distance):
    '''
    locate nearby buildings with target amenity value of a given Polygon building, within some distance N, S, E, W of the centroid of it.
    :param centerBuild: the given building, dictionary element in the returned list of fun: getBuildingswithType
    :param targetAmenity: the amenity value of target surrounding buildings
    :param distance: distance in meters, N, S, E, W of the point.
    :return: GeoDataFrame of targetBuildings
    '''
    geometry = centerBuild['geometry']
    centroid = getPolygonCentr(geometry)
    lon = centroid.x
    lat = centroid.y
    tags = {'amenity':targetAmenity}
    targetBuildings = osmnx.pois.pois_from_point((lat, lon), tags, dist=distance)
    return targetBuildings
