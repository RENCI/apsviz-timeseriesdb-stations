#!/usr/bin/env python

# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

# coding: utf-8

# Import Python modules
import argparse
import glob
import os
import sys
import shutil
import psycopg
import pandas as pd
from pathlib import Path
from loguru import logger

def ingestStations(ingestDir):
    ''' This function takes as input an ingest directory. The input directory is used to search for geom stations files
        that are to be ingested. The ingest directory is used to define the path of the file to be ingested. The
        ingest directory is the directory path in the apsviz-timeseriesdb database container. 
        Parameters
            ingestDir: string
                Directory path to ingest data files, created from the harvest files. 
        Returns 
            None
    '''         

    # Move station meta files to the /data/DataIngesting/DAILY_INGEST/
    logger.info('Copy stations directory to '+ingestDir)
    shutil.copytree('/home/nru/stations', ingestDir+'stations', dirs_exist_ok=True)

    # Create list of geom files, to be ingested by searching the input directory for geom files.
    inputFiles = glob.glob(ingestDir+"stations/geom_*.csv")
            
    # Define the ingest path and file using the ingest directory and the geom file name

    try:
        # Create connection to database, set autocommit, and get cursor
        with psycopg.connect(dbname=os.environ['APSVIZ_GAUGES_DB_DATABASE'],
                             user=os.environ['APSVIZ_GAUGES_DB_USERNAME'],
                             host=os.environ['APSVIZ_GAUGES_DB_HOST'],
                             port=os.environ['APSVIZ_GAUGES_DB_PORT'],
                             password=os.environ['APSVIZ_GAUGES_DB_PASSWORD'],
                             autocommit=True) as conn:
            cur = conn.cursor()

            # Loop thru geom file list, ingesting each one
            for geomFile in inputFiles:
                # Run query
                with open(geomFile, "r") as f:
                    with cur.copy("COPY drf_gauge_station (station_name,lat,lon,tz,gauge_owner,location_name,location_type,country,state,county,geom) FROM STDIN WITH (FORMAT CSV)") as copy:
                        while data := f.read(100):
                            copy.write(data)

            # Close cursor and database connection
            cur.close()
            conn.close()

    # If exception log error
    except (Exception, psycopg.DatabaseError) as error:
        logger.exception(error)

def ingestObsSourceData(ingestDir):
    ''' This function takes as input an ingest directory. It uses the input directory to search for source CSV files, that where
        created by the createIngestObsSourceMeta.py program. It uses the ingest directory to define the path of the file that is to
        be ingested. The ingest directory is the directory path in the apsviz-timeseriesdb database container.
        Parameters
            ingestDir: string
                Directory path to ingest data files, created from the harvest files.
        Returns 
            None
    '''         
            
    # Create list of source files, to be ingested by searching the input directory for source files.
    inputFiles = glob.glob(ingestDir+"source_*.csv")
            
    try:
        # Create connection to database, set autocommit, and get cursor
        with psycopg.connect(dbname=os.environ['APSVIZ_GAUGES_DB_DATABASE'],
                             user=os.environ['APSVIZ_GAUGES_DB_USERNAME'], 
                             host=os.environ['APSVIZ_GAUGES_DB_HOST'], 
                             port=os.environ['APSVIZ_GAUGES_DB_PORT'],
                             password=os.environ['APSVIZ_GAUGES_DB_PASSWORD'],
                             autocommit=True) as conn:
            cur = conn.cursor()

            # Loop thru source file list, ingesting each one
            for sourceFile in inputFiles:
                # Run ingest query
                with open(sourceFile, "r") as f:
                    with cur.copy("COPY drf_gauge_source (station_id,data_source,source_name,source_archive,units) FROM STDIN WITH (FORMAT CSV)") as copy:
                        while data := f.read(100):
                            copy.write(data)

                # Remove source data file after ingesting it.
                logger.info('Remove source data file: '+sourceFile+' after ingesting it')
                os.remove(sourceFile)

            # Close cursor and database connection
            cur.close()
            conn.close()

    # If exception log error
    except (Exception, psycopg.DatabaseError) as error:
        logger.exception(error)

def ingestModelSourceData(ingestDir):
    ''' This function takes as input an ingest directory. It uses the input directory to search for source CSV files, that where
        created by the createIngestModelSourceMeta.py program. It uses the ingest directory to define the path of the file that is to
        be ingested. The ingest directory is the directory path in the apsviz-timeseriesdb database container.
        Parameters
           ingestDir: string
                Directory path to ingest data files, created from the harvest files.
        Returns
            None
    '''

    # Create list of source files, to be ingested by searching the input directory for source files.
    inputFiles = glob.glob(ingestDir+"source_*.csv")

    try:
        # Create connection to database, set autocommit, and get cursor
        with psycopg.connect(dbname=os.environ['APSVIZ_GAUGES_DB_DATABASE'], 
                             user=os.environ['APSVIZ_GAUGES_DB_USERNAME'], 
                             host=os.environ['APSVIZ_GAUGES_DB_HOST'], 
                             port=os.environ['APSVIZ_GAUGES_DB_PORT'], 
                             password=os.environ['APSVIZ_GAUGES_DB_PASSWORD'], 
                             autocommit=True) as conn:
            cur = conn.cursor()

            # Loop thru source file list, ingesting each one
            for sourceFile in inputFiles:
                # Run ingest query
                with open(sourceFile, "r") as f:
                    with cur.copy("COPY drf_model_source (station_id,data_source,source_name,source_archive,source_instance,forcing_metclass,units) FROM STDIN WITH (FORMAT CSV)") as copy:
                        while data := f.read(100):
                            copy.write(data)

                # Remove source data file after ingesting it.
                logger.info('Remove source data file: '+sourceFile+' after ingesting it')
                os.remove(sourceFile)

            # Close cursor and database connection
            cur.close()
            conn.close()

    # If exception log error
    except (Exception, psycopg.DatabaseError) as error:
        logger.exception(error)

# Main program function takes args as input, which contains the inputDir, inputTask, inputDataSource, inputSourceName, and inputSourceArchive values.
@logger.catch
def main(args):
    ''' Main program function takes args as input, starts logger, and runs specified task.
        Parameters
            args: dictionary
                contains the parameters listed below.
            inputTask: string
                The type of task (ingestStations, ingestObsSourceData, ingestModelSourceData ) 
                to be perfomed. The type of inputTask can change what other types of inputs ingestTask.py requires. Below is a list of all inputs, with associated tasks.
            ingestDir: string
                Directory path to ingest data files, created from the harvest files. Used by ingestStations, ingestObsSourceData, and ingestModelSourceData.
        Returns
            None
    '''

    # Add logger
    logger.remove()
    log_path = os.path.join(os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs')), '')
    logger.add(log_path+'ingestObsTasks.log', level='DEBUG')
    logger.add(sys.stdout, level="DEBUG")
    logger.add(sys.stderr, level="ERROR")

    inputTask = args.inputTask

    # Check if inputTask if file, station, source, data or view, and run appropriate function
    if inputTask.lower() == 'ingeststations':
        ingestDir = os.path.join(args.ingestDir, '')
        logger.info('Ingesting station data.')
        ingestStations(ingestDir)
        logger.info('Ingested station data.')
    elif inputTask.lower() == 'ingestobssourcedata':
        ingestDir = os.path.join(args.ingestDir, '')
        logger.info('Ingesting obs source data.')
        ingestObsSourceData(ingestDir)
        logger.info('ingested obs source data.')
    elif inputTask.lower() == 'ingestmodelsourcedata':
        ingestDir = os.path.join(args.ingestDir, '')
        logger.info('Ingesting model source data.')
        ingestModelSourceData(ingestDir)
        logger.info('ingested model source data.')

# Run main function takes inputDir, inputTask, inputDataSource, inputSourceName, and inputSourceArchive as input.
if __name__ == "__main__":
    ''' Takes argparse inputs and passes theme to the main function
        Parameters
            inputTask: string
                The type of task (ingestStations, ingestObsSourceData, ingestModelSourceData
            ingestDir: string
                Directory path to ingest data files, created from the harvest files. Used by ingestStations, ingestObsSourceData, and ingestModelSourceData.
        Returns
            None
    '''         

    # parse input arguments
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("--inputTask", help="Input task to be done", action="store", dest="inputTask", choices=['ingestStations','ingestObsSourceData','ingestModelSourceData'], required=True)
    parser.add_argument("--ingestDIR", "--ingestDir", help="Ingest directory path", action="store", dest="ingestDir", required=True)

    # Parse arguments
    args = parser.parse_args()

    # Run main
    main(args)