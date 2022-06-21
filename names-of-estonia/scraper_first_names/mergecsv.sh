#!/bin/bash

OutFileName="uniquefirstnames.csv"                       # Fix the output name
i=0                                       # Reset a counter
for filename  in ./*.csv; do 
 echo $filename ;
 if [ "$filename"  != "$OutFileName" ] ;      # Avoid recursion 
 then 
   tail -n +2  $filename >>  $OutFileName # Append from the 2nd line each file
   i=$(( $i + 1 ))                        # Increase the counter
 fi
done

cut -f 2 -d ',' $OutFileName | grep -v '^[А-Яа-яЁё]' | grep -v "'" | sort -o $OutFileName -u # filter first names

