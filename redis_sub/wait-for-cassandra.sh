#!/bin/sh

cassandra_status=0
retries=0

while [ $cassandra_status -eq 0 ] && [ $retries -lt 60 ]
do
   echo "Checking if Cassandra is up and running ..."

   cassandra_status=`ping cassandra -c 3`

   if [ ! -z "$cassandra_status" -a "$cassandra_status" != " " ]
   then
       cassandra_status=1;
   else
       cassandra_status=0;
       retries = $retries + 1
       sleep 1
   fi

done

if [ $cassandra_status -eq 0 ]; then
        echo "/!\ ERROR: unable to connect to Cassandra. Tried for 60 ;"
        exit 1
      else
        echo "Cassandra startup completed successfully --- OK"
        exit 0
fi
