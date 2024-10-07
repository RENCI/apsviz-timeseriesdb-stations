<!--
SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.

SPDX-License-Identifier: GPL-3.0-or-later
SPDX-License-Identifier: LicenseRef-RENCI
SPDX-License-Identifier: MIT
-->

# apsviz-timeseriesdb-stations 
The software, in this repo, is used to ingest gauge station data from NOAA, NCEM, NDBC, and ADICIRC into the apsviz-timeseriesdb. The the repo for the apsviz-timeseriesdb is at:  

https://github.com/RENCI/apsviz-timeseriesdb  

## Create Geom file

To ingest a new station the first thing that needs to be done is to create a geom file containing the station meta-data and add it to the station directory in this repo:  

apsviz-timeseriesdb-stations/stations  

The file needs to begin with geom for example for a NOAA station the file name would be:  

geom_noaa_stations.csv  

The file needs to contain the following data:  

8725114,26.1366666667,-81.7883333333,gmt,NOAA/NOS,Naples Bay,tidal,us,fl,Collier,0101000020E6100000B137A70D747254C009EE2F96FC223A40  

Where the columns above are:  

station_name: 8725114  
lat: 26.1366666667  
lon: -81.7883333333  
tz: gmt  
gauge_owner: NOAA/NOS  
location_name: Naples Bay  
location_type: tidal  
country: us  
state: fl  
county: Collier  
geom: 0101000020E6100000B137A70D747254C009EE2F96FC223A40  

This file needs to be created before you build the Docker image and create the Docker container.  The data in this file will be ingested into the drf_gauge_station data, which is described in the "Ingest New Station into Database" section of this document.  

## Install apsviz-timeseriesdb-stations  

To install apsviz-timeseriesdb-stations you first need to clone it:  

git clone https://github.com/RENCI/apsviz-timeseriesdb-stations.git  

Then change your directory to apsviz-timeseriesdb-stations/build:  

cd apsviz-timeseriesdb-stations/build  

From this directory you can run the build.sh file as follows:  

./build.sh latest  

After the build has finished edit the createcontainer.sh file, adding the directory path you want to add as a volume:  

\#!/bin/bash  
\# setup specific to apsviz_timeseriesdb_stations   
version=$1;   

docker run -ti --name apsviz_timeseriesdb_stations_$version \\  
  --volume /xxxx/xxxx/xxxx:/data \\  
  -d apsviz_timeseriesdb_stations:$version /bin/bash  

The xxxx represent directories in your directory path, so replace them with the actual directory names. The directory you add as a volume should have enough storage space to do the job. After editing createcontainer.sh run it:  

createcontainer.sh latest  

The value 'latest' in the above commands is the version of the docker image and container you are creating. You can use values other than 'latest', but make sure you use the same values in all the commands.  

The next step is to make a network link to apsviz-timeseriesdb_default. This step will enable you to access the apsviz-timeseriesdb database. Before taking this step you have to install apsviz-timeseriesdb. If you have not install apsviz-timeseriesdb go to the following URL for instructions:  

https://github.com/RENCI/apsviz-timeseriesdb  

To create the network link run the createnetwork.sh file as follows:  

./createnetwork.sh latest  

## Ingest New Station into Database

Before ingesting new station data make sure you have created a geom that contains the station(s) meta-data as described in section "Create Geom file" of this document.  

To ingest a new station(s) there are three steps. First the station(s) meta-data needs to be ingested into the drf_gauge_station table. Then the Observation source information for the new station(s) needs to be ingested into the drf_gauge_source table. Finally, the Model source information for the new station(s) needs to be ingested into the drf_model_source table.  

To ingest the station data into the drf_gauge_station table run the following command:  

python ingestTasks.py --ingestDir /data/ast-run-ingester/ --inputTask ingestStations  

To ingest the Observation source data into the drf_gauge_source table run the following command:  

python createIngestNewObsSourceMeta.py --ingestDir /data/ast-run-ingester/ --inputLocationType tidal  

To ingest the Model source data into the drf_model_source table run the following command:  

python createIngestNewModelSourceMeta.py --ingestDir /data/ast-run-ingester/ --inputLocationType tidal  


