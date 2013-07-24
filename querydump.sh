#!/bin/bash

dumpdir=/data/querydump

while true;  do
  ts=`date +%s`
  dumpfile=$dumpdir/dump-$ts.log

  threads=`/usr/bin/mysqladmin status | awk '{print $4}'`

  #echo $threads
  if [ "$threads" -gt 50 ]; then
	echo $threads >  $dumpfile
	/usr/bin/mysql -e "show full processlist\G" >> $dumpfile
  fi

  sleep 1;
done
