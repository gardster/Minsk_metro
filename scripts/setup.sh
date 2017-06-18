

mkdir -p ../deps/osmconvert
pushd ../deps/osmconvert
wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert
popd

mkdir -p ../deps/osrm
pushd ../deps/osrm
git clone git://github.com/Project-OSRM/osrm-backend ./
mkdir build
cd build
cmake ../
make -j
popd

mkdir -p ../deps/osm2pgsql
pushd ../deps/osm2pgsql
git clone git://github.com/openstreetmap/osm2pgsql.git ./
mkdir build
cd build
cmake ../
make -j
popd
