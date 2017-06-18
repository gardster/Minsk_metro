
# Get initial file
mkdir -p ../data
pushd ../data
#wget http://download.geofabrik.de/europe/belarus-latest.osm.pbf
../deps/osmconvert/osmconvert -b=27.4,53.82,27.75,54.0 belarus-latest.osm.pbf --out-pbf > belarus-clipped.osm.pbf
popd
