<!--
SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.

SPDX-License-Identifier: GPL-3.0-or-later
SPDX-License-Identifier: LicenseRef-RENCI
SPDX-License-Identifier: MIT
-->

# apsviz-timeseriesdb-stations 
The software, in this repo, is used to ingest gauge station data from NOAA, NCEM, NDBC, and ADICIRC. To begin ingesting station data, you first need to install the apsviz-timeseriesdb repo which can bet downloaded from:  

https://github.com/RENCI/apsviz-timeseriesdb  

Follow the installation instructions for that repo. It creates and postgesql database, that serves data using a Django Rest Framework (DRF) app. 

The gauge data that is being ingested can currently be accessed from the apsviz-timeseriesdb.edc.renci.org VM in the following directory:   

/projects/ees/TDS/DataHarvesting/DAILY_HARVESTING/ 

It was generated using the software in the ADCIRC Support Tools (AST) repo, which can be downloaded from:  

https://github.com/RENCI/AST

## Install apsviz-timeseriesdb-stations

To install apsviz-timeseriesdb-stations you first need to clone it:

git clone https://github.com/RENCI/apsviz-timeseriesdb-stations.git

Next edit the run/env file adding a password to the line:

SQL_PASSWORD=xxxxxx

where you change xxxxxx to the password that is used to access the database in apsviz-timeseriesdb.

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

## Ingest original station data

In the next step the original station data is ingested into the database. This data was obtained directly from NOAA, NDBC and NCEM, and is used to generate the stations data that will be ingested into the drf_gauge_station table, which is described further down in this README.md.

To ingest the original stations data change your directory to:

cd original_gauge_ingest

Create a file named .env.db in this directory, with the following information:

POSTGRES_USER=apsviz_gauges
POSTGRES_PASSWORD=xxxxxx
POSTGRES_DB=apsviz_gauges

where you change xxxxxx to the password that is used to access the database in apsviz-timeseriesdb.

Then copy the CSV files to container:

./docker_cp_csv.sh

Then create original station tables by running:

./psql_original_gauge_create.sh

Finally ingest original station data by running:

./psql_original_gauge_ingest.sh

## Ingest Data into Database

At this point things are installed, and you can access the apsviz_timeseriesdb_ingest container shell using the root_shell.sh file as follows:

./root_shell.sh latest
 
The first step is to make sure you have created a directory to store the files that you are going to be creating. From within the apsviz_timeseriesdb_ingest shell make the following directories:

mkdir -p /data/DataIngesting/DAILY_INGEST

If you are running on you local machine also make sure you have downloaded the harvest files from the directory:

/projects/ees/TDS/DataHarvesting/DAILY_HARVESTING/

on the apsviz-timeseriesdb.edc.renci.org VM, to the same location that you added as a volume when create the container, so that when you are in the container the following directory exits:

/data/DataIngesting/DAILY_HARVESTING/

### Create and Ingest Station Data 

To ingest the station data, first make sure you have already ingested the original station data, as describe above in this README.md. You also need to have installed the apsviz-timeseriesdb repo:

https://github.com/RENCI/apsviz-timeseriesdb

To create the station meta data that will be ingested into the drf_gauge_station table, in the apsviz-timeseriesdb database, run the following command in the /home/nru directory:

python runIngest.py --outputDir /data/DataIngesting/DAILY_INGEST --inputTask CreateStations

This will create Station data files in /data/DataIngesting/DAILY_INGEST. The next step is to ingest them into the drf_gauge_station table in the apsviz-timeseriesdb database. To do this run the following command in the /home/nru directory:

python runIngest.py --inputDIR /data/DataIngesting/DAILY_INGEST --ingestDir /home/DataIngesting/DAILY_INGEST --inputTask IngestStations

