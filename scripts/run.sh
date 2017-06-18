
# Get initial file
mkdir -p ../data
pushd ../data
#wget http://download.geofabrik.de/europe/belarus-latest.osm.pbf
#../deps/osmconvert/osmconvert -b=27.4,53.82,27.75,54.0 belarus-latest.osm.pbf --out-pbf > belarus-clipped.osm.pbf
popd

#../deps/osrm/build/osrm-extract -p ../deps/osrm/profiles/foot.lua ../data/belarus-clipped.osm.pbf
#../deps/osrm/build/osrm-contract ../data/belarus-clipped.osrm

../deps/osm2pgsql/build/osm2pgsql -c ../data/belarus-clipped.osm.pbf  -d public -U levdragunov -H localhost  -l -s -S ../deps/osm2pgsql/default.style -x
