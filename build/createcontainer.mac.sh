#!/bin/bash
# setup specific to apsviz_timeseriesdb_stations 
version=$1;

docker run -ti --name apsviz_timeseriesdb_stations_$version \
  --volume /Users/jmpmcman/Work/Surge/data:/data \
  -d apsviz_timeseriesdb_stations:$version /bin/bash 
