import psycopg2
import requests
import json

def get_travel_time(point1, point2):
    r = requests.get('http://localhost:5000/route/v1/driving/{},{};{},{}'.format(point1[0], point1[1], point2[0], point2[1]))
    data = r.json()
    return data["routes"][0]["duration"]

def get_points_around(cursor, point):
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
    cursor.execute('''
        select max(st_x(way)), min(st_x(way)), max(st_y(way)), min(st_y(way)) from planet_osm_point
        where
            st_intersects(way, ST_Buffer(ST_SetSRID(ST_GeomFromGeoJSON('{}'),4326), 0.02));
    '''.format(point))
    result = []
    for row in cursor:
        maxx= int(row[0]*1000)*10
        minx= int(row[1]*1000)*10
        maxy= int(row[2]*1000)*10
        miny= int(row[3]*1000)*10
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
