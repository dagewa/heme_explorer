#!/bin/bash

# Get structures
if [ ! -d heme ]; then
    mkdir -p heme
    cd heme
    wget --input-file=../heme_cif_urls.txt
    for f in *.icif; do
      mv -- "$f" "${f%.icif}.cif"
    done
    cd ..
fi

# Analyse structures
mkdir -p analysis
cd analysis
ccp4-python ../classify.py ../heme > heme_data.txt
grep -v "Can't" heme_data.txt > heme_data_readable.txt
Rscript --vanilla ../render.r heme_data_readable.txt
cd ..

# Make website
mkdir -p build
cd build
cp ../analysis/index.html .
cp -r ../uglymol .
cd ..
echo "Built page in build/index.html"
