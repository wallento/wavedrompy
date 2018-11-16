#!/bin/bash -e

for file in $( ls *.json )
do
    echo "Processing $file"
    rm -f ${file%.json}.{svg,pdf,png}
    wavedrompy -i $file -s ${file%.json}.svg
    rsvg-convert ${file%.json}.svg -f pdf -o ${file%.json}.pdf
    rsvg-convert ${file%.json}.svg -f png -o ${file%.json}.png
done

echo "Test complete"
