#! /bin/sh

for file in $( ls *.json )
do
    echo "Processing $file"
    ../src/wavedrom.py source $file svg ${file%.json}.svg
done

echo "Test complete"
