
# Get initial file
mkdir -p ../data
pushd ../data
wget http://download.geofabrik.de/europe/belarus-latest.osm.pbf
../deps/osmconvert/osmconvert -b=27.4,53.82,27.75,54.0 belarus-latest.osm.pbf --out-pbf > belarus-clipped.osm.pbf
popd

# Prepare OSRM
../deps/osrm/build/osrm-extract -p ../deps/osrm/profiles/foot.lua ../data/belarus-clipped.osm.pbf
../deps/osrm/build/osrm-contract ../data/belarus-clipped.osrm

# And run it
../deps/osrm/build/osrm-routed ../data/belarus-clipped.osrm &

# Prepare osm in the database
../deps/osm2pgsql/build/osm2pgsql -c ../data/belarus-clipped.osm.pbf  -d public -U levdragunov -H localhost  -S ../deps/osm2pgsql/default.style

psql -d public -U levdragunov -H localhost  -f init_db.sql
#python3 calculate.py
#psql -f delete_duplicates.sql
#psql -f create_polygons.sql
#python3 generate_geojson.py
