import json
import psycopg2

connection = psycopg2.connect('host=localhost user=levdragunov dbname=postgres')
cursor = connection.cursor()

cursor.execute('select duration, ST_AsGeoJSON(geom) from minsk_areas')

result = {
  "type": "FeatureCollection",
  "features": [
  ]
}

for row in cursor:
    feature = {
      "type": "Feature",
      "properties": {
          "duration": row[0]
          },
      "geometry": json.loads(row[1])
      }
    result["features"].append(feature)

with open("data/metro.json", "w") as f:
    f.write('metro = {}'.format(json.dumps(result)))
