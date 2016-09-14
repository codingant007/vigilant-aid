#!/bin/bash

downloadUrl="http://image-net.org/image/ILSVRC2015/ILSVRC2015_DET_test_new.tar.gz"
if [ $# -eq 1 ]
	then
		downloadUrl=$1
fi
echo $downloadUrl
exit
contentLength=`curl --head $downloadUrl | grep 'Content-Len' | sed 's/^.*Content.*Length: \([0-9]*\).*$/\1/'`
echo "contentLegnth: $contentLength"
function download_range {
	echo "part: $3 --- $1 - end: $2"
	partName="ppart$3"
	echo $partName
	curl --range $1-$2 -o $partName $downloadUrl
}

# 100MB blocks
blockSize=99999999999																																																																																																																																																																																																																																																																																																																																					
part=0
for (( c=0; c<$contentLength-$blockSize; c=c+$blockSize+1))
do
	start=$c
	end=$(($c+$blockSize))
	part=$(($part+1))
	download_range $start $end $part
done

#echo $(($part*$(($blockSize+1))))
# Reminder block
download_range $(($part*$(($blockSize+1)))) $contentLength $(($part+1))

