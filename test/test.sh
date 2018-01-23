#! /bin/sh

for file in $( ls *.json )
do
    echo "Processing $file"
    rm ${file%.json}.svg
    python3 ../wavedrompy/wavedrom.py -i $file -s ${file%.json}.svg
done

echo "Test complete"
