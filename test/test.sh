#! /bin/sh

for file in $( ls *.json )
do
    echo $file
    ../src/wavedrom.py source $file svg ${file%.json}.svg
done
