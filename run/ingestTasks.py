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
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# This function takes an input directory and an ingest directory as input. The input directory is used to search for geom 
# station files that are to be ingested. The ingest directory is used to define the path of the file to be ingested. The 
# ingest directory is the directory path in the apsviz-timeseriesdb database container.
def ingestStation(inputDir, ingestDir):
    # Create list of geom files, to be ingested by searching the input directory for geom files.
    inputFiles = glob.glob(inputDir+"geom_*.csv")

    # Loop thru geom file list, ingesting each one 
    for geomFile in inputFiles:
        # Define the ingest path and file using the ingest directory and the geom file name
        ingestPathFile = ingestDir+Path(geomFile).parts[-1]
 
        try:
            # Create connection to database and get cursor
            conn = psycopg2.connect(dbname=os.environ['SQL_DATABASE'], user=os.environ['SQL_USER'], host=os.environ['SQL_HOST'], port=os.environ['SQL_PORT'], password=os.environ['SQL_PASSWORD'])
            cur = conn.cursor()

            # Set enviromnent
            cur.execute("""SET CLIENT_ENCODING TO UTF8""")
            cur.execute("""SET STANDARD_CONFORMING_STRINGS TO ON""")
            cur.execute("""BEGIN""")

            # Run query
            cur.execute("""COPY drf_gauge_station(station_name,lat,lon,tz,gauge_owner,location_name,location_type,country,state,county,geom)
                           FROM %(ingest_path_file)s
                           DELIMITER ','
                           CSV HEADER""",
                        {'ingest_path_file': ingestPathFile})

            # Commit ingest
            conn.commit()
 
            # Close cursor and database connection
            cur.close()
            conn.close()

        # If exception log error
        except (Exception, psycopg2.DatabaseError) as error:
            logger.info(error)


# Main program function takes args as input, which contains the inputDir, ingestDir, inputTask, inputDataSource, inputSourceName, and inputSourceArchive values.
@logger.catch
def main(args):
    # Add logger
    logger.remove()
    log_path = os.path.join(os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs')), '')
    logger.add(log_path+'ingestTasks.log', level='DEBUG')
    logger.add(sys.stdout, level="DEBUG")
    logger.add(sys.stderr, level="ERROR")

    # Extract args variables
    inputDir = os.path.join(args.inputDir, '')

    ingestDir = os.path.join(args.ingestDir, '')

    logger.info('Create station data.')
    ingestStation(inputDir, ingestDir)
    logger.info('Created station data.')

# Run main function takes inputDir, ingestDir, inputTask, inputDataSource, inputSourceName, and inputSourceArchive as input.
if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("--inputDIR", "--inputDir", help="Input directory path", action="store", dest="inputDir", required=True)
    parser.add_argument("--ingestDIR", "--ingestDir", help="Ingest directory path", action="store", dest="ingestDir", required=True)

    # Parse arguments
    args = parser.parse_args()

    # Run main
    main(args)

