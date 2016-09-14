#!/bin/bash
no_of_parts=10
str=""
for((c=1; c<=$no_of_parts; c++ ))
do
	str=$str"part"$c" "
done
echo "cat $str"
cat `echo "$str"` > concated.tar.gz
