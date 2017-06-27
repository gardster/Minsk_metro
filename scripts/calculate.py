import psycopg2
import requests
import json

def get_travel_time(point1, point2):
    r = requests.get('http://localhost:5000/route/v1/driving/{},{};{},{}'.format(point1[0], point1[1], point2[0], point2[1]))
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
    maxx= int(point['coordinates'][0]*1000)*10 + 200
    minx= int(point['coordinates'][0]*1000)*10 - 200
    maxy= int(point['coordinates'][1]*1000)*10 + 200
    miny= int(point['coordinates'][1]*1000)*10 - 200
    while minx < maxx:
        cury = miny
        while cury < maxy:
            result.append(json.dumps({"type":"Point","coordinates":[float(minx)/10000.0, float(cury)/10000.0]}))
            cury += 5
        minx += 5
    return result

connection = psycopg2.connect('')
cursor = connection.cursor()

cursor.execute("select ST_AsGeoJSON(way) from planet_osm_point where railway='subway_entrance';")

points = []
for row in cursor:
    points.append(row[0])

result = []
for metro_point in points:
    p1 = json.loads(metro_point)
    round_points = get_points_around_grid(cursor, metro_point)
    for round_point in round_points:
        p2 = json.loads(round_point)
        dt = get_travel_time(p1['coordinates'], p2['coordinates'])
        result.append((round_point, dt))


cursor.execute('insert into minsk_points (point, duration) values {}'.format(','.join(["(ST_SetSRID(ST_GeomFromGeoJSON('{}'),4326), {})".format(p[0], p[1]) for p in result])))
connection.commit()
