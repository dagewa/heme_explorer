#!/bin/bash
if [ ! -d heme ]; then
    mkdir -p heme
    cd heme
    wget --input-file=../heme_cif_urls.txt
    for f in *.icif; do
      mv -- "$f" "${f%.icif}.cif"
    done
    cd ..
fi

mkdir -p analysis
cd analysis
ccp4-python ../classify.py ../heme > heme_distances.txt
grep -v "Can't" heme_distances.txt > heme_distances_readable.txt
Rscript --vanilla ../plots.R heme_distances_readable.txt
cd ..
