

mkdir -p ../deps/osmconvert
pushd ../deps/osmconvert
wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert
popd

