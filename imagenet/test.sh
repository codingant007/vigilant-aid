#!/bin/bash

function test {
	sleep 1
}

START=$(date +%s);

for ((i=0; i<10; i++))
do
	test&
	test&
	test&
	test&
	if (( i % 2 == 0 )); then
		END=$(date +%s);
		echo -n $i" at "
		echo $((END-START)) | awk '{print int($1/60)"min:"int($1%60)"sec"}'
		wait
	fi
done
END=$(date +%s);
echo $((END-START)) | awk '{print "Program completed at "int($1/60)"min:"int($1%60)"sec"}'