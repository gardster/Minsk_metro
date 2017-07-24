import psycopg2
import requests
import json
import math

def _c3857t4326(lon, lat):
    """
    Pure python 3857 -> 4326 transform. About 12x faster than pyproj.
    """
    xtile = lon / 111319.49079327358
    ytile = math.degrees(
        math.asin(math.tanh(lat / 20037508.342789244 * math.pi)))
    return(xtile, ytile)

def get_travel_time(point1, point2):
    lon1, lat1 = _c3857t4326(point1[0], point1[1])
    lon2, lat2 = _c3857t4326(point2[0], point2[1])
    r = requests.get('http://localhost:5000/route/v1/driving/{},{};{},{}'.format(lon1, lat1, lon2, lat2))
    data = r.json()
    return data["routes"][0]["duration"]

def get_points_around(cursor, point):
    # Case with points from the database
    cursor.execute('''
        select st_asgeojson(way) from planet_osm_point
        where
            st_intersects(way, ST_Buffer(ST_SetSRID(ST_GeomFromGeoJSON('{}'),4326), 0.02));
    '''.format(point))
    result = []
    for row in cursor:
        result.append(row[0])
    return result

def get_points_around_grid(cursor, point):
    # Case with lon-lat grid. Only for demo purpose. Please use web mercator grid for the better picture.
    result = []
    mainx = int(point['coordinates'][0]/25)*25
    mainy = int(point['coordinates'][1]/25)*25
    maxx= int(mainx) + 2200
    minx= int(mainx) - 2200
    maxy= int(mainy) + 2200
    miny= int(mainy) - 2200
    while minx < maxx:
        cury = miny
        while cury < maxy:
            result.append(json.dumps({"type":"Point","coordinates":[minx, cury]}))
            cury += 25
        minx += 25
    return result

connection = psycopg2.connect('host=localhost user=levdragunov dbname=postgres')
cursor = connection.cursor()

cursor.execute("select ST_AsGeoJSON(way) from planet_osm_point where railway='subway_entrance';")

points = []
for row in cursor:
    points.append(row[0])

result = []
for i, metro_point in enumerate(points):
    print("{}/{}".format(i, len(points)))
    p1 = json.loads(metro_point)
    round_points = get_points_around_grid(cursor, p1)
    for round_point in round_points:
        p2 = json.loads(round_point)
        dt = get_travel_time(p1['coordinates'], p2['coordinates'])
        result.append((round_point, dt))


cursor.execute('insert into minsk_points (point, duration) values {}'.format(','.join(["(ST_SetSRID(ST_GeomFromGeoJSON('{}'),3857), {})".format(p[0], p[1]) for p in result])))
connection.commit()
