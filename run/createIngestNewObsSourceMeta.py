#!/usr/bin/env python
# coding: utf-8

# Import python modules
import argparse
import glob
import sys
import os
import psycopg
import pandas as pd
import subprocess
from loguru import logger

def getSourceObsMetaLocationType(inputLocationType):
    ''' Returns DataFrame containing source meta-data queried from the drf_source_obs_meta table.
        Parameters
            inputLocationType: string
                gauge location type (COASTAL, TIDAL, or RIVERS)
        Returns
            DataFrame
    '''

    try:
        # Create connection to database and get cursor
        conn = psycopg.connect(dbname=os.environ['APSVIZ_GAUGES_DB_DATABASE'],
                               user=os.environ['APSVIZ_GAUGES_DB_USERNAME'],
                               host=os.environ['APSVIZ_GAUGES_DB_HOST'],
                               port=os.environ['APSVIZ_GAUGES_DB_PORT'],
                               password=os.environ['APSVIZ_GAUGES_DB_PASSWORD'])
        cur = conn.cursor()

        # Run query
        cur.execute("""SELECT data_source, source_name, source_archive, source_variable, filename_prefix, location_type, units
                       FROM drf_source_obs_meta WHERE location_type =  %(locationtype)s
                       ORDER BY filename_prefix""",
                    {'locationtype': inputLocationType})

        # convert query output to Pandas dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['data_source', 'source_name', 'source_archive', 'source_variable', 'filename_prefix', 'location_type', 'units'])

        # Close cursor and database connection
        cur.close()
        conn.close()

        # return DataFrame
        return(df)

    # If exception log error
    except (Exception, psycopg.DatabaseError) as error:
        logger.exception(error)

def getStationID(stationNameList):
    ''' Returns a DataFrame containing a list of station ids and station names, based on the location type (COASTAL, TIDAL or RIVERS),
        from table drf_gauge_station.
        Parameters
            stationNameList: list
                a list of station_names
        Returns
            DataFrame
    '''

    try:
        # Create connection to database and get cursor
        conn = psycopg.connect(dbname=os.environ['APSVIZ_GAUGES_DB_DATABASE'],
                               user=os.environ['APSVIZ_GAUGES_DB_USERNAME'],
                               host=os.environ['APSVIZ_GAUGES_DB_HOST'],
                               port=os.environ['APSVIZ_GAUGES_DB_PORT'],
                               password=os.environ['APSVIZ_GAUGES_DB_PASSWORD'])
        cur = conn.cursor()

        # Run query
        cur.execute("""SELECT station_id, station_name FROM drf_gauge_station
                       WHERE station_name = ANY(%(stationnamelist)s)
                       ORDER BY station_name""",
                    {'stationnamelist': stationNameList})

        # convert query output to Pandas dataframe
        df = pd.DataFrame(cur.fetchall(), columns=['station_id', 'station_name'])

        # Close cursor and database connection
        cur.close()
        conn.close()

        # Return Pandas dataframe
        return(df)

    # If exception log error
    except (Exception, psycopg.DatabaseError) as error:
        logger.exception(error)

def addMeta(ingestDir,inputFilePath, inputDataSource, inputSourceName, inputSourceArchive, inputUnits, inputLocationType):
    ''' Returns a CSV file that containes source information specific to station IDs that have been extracted from the drf_gauge_station table.
        The function adds additional source information (data source, source name, source archive, data units) to the station IDs. This 
        information is latter ingested into table drf_gauge_source by running the ingestObsSourceData() function in ingetTask.py
        Parameters
            ingestDir: string
                 Directory path to the ast-run-ingester directory
            inputFilePath: string
                The geom file path and name
            inputDataSource: string
                Unique identifier of data source (e.g., river_gauge, tidal_predictions, air_barameter, wind_anemometer...)
            inputSourceName: string
                Organization that owns original source data (e.g., ncem, ndbc, noaa...)
            inputSourceArchive: string
                Where the original data source is archived (e.g., contrails, ndbc, noaa...)
            inputUnits: string
                Units of data (e.g., m (meters), m^3ps (meter cubed per second), mps (meters per second), and mb (millibars)
            inputLocationType: string
                gauge location type (COASTAL, TIDAL, or RIVERS)
        Returns
            CSV file
    '''

    # Add station csv file as input and change this to read station csv file
    # Create list of geom files, to be ingested by searching the input directory for geom files.
    df = pd.read_csv(inputFilePath, usecols=[0], names=['station_name'])
    stationNameList = [format(x, 'd') for x in list(df['station_name'].values)]
    df = getStationID(stationNameList)

    df['data_source'] = inputDataSource
    df['source_name'] = inputSourceName
    df['source_archive'] = inputSourceArchive
    df['units'] = inputUnits

    # Drop station_name from DataFrame 
    df.drop(columns=['station_name'], inplace=True)

    # Reorder column name and update indeces 
    newColsOrder = ['station_id','data_source','source_name','source_archive','units']
    df=df.reindex(columns=newColsOrder)

    # Write dataframe to csv file 
    outputFile = 'source_'+inputSourceName+'_stationdata_'+inputSourceArchive+'_'+inputLocationType+'_'+inputDataSource+'_meta.csv'
    df.to_csv(ingestDir+outputFile, index=False, header=False)

def runIngestObsSourceData(ingestDir, inputLocationType):
    ''' This function runs createIngestObsSourceMeta.py which creates source data files that are then ingested into the drf_gauge_source
        table, in the database, by running ingestObsTasks.py using --inputTask ingestObsSourceData.
        Parameters
            ingestDir: string
                Directory path to the ast-run-ingester directory
            inputLocationType: string
                Gauge location type (COASTAL, TIDAL, or RIVERS)
        Returns              
            None, but it runs createIngestObsSourceMeta.py, which creates CSV files containing source meta-data, and then runs
            ingestObsTasks.py which ingest the CSV file into the drf_gauge_source table.
    '''
 
    # get source meta
    df = getSourceObsMetaLocationType(inputLocationType)

   # get geom file
    inputFile = glob.glob(ingestDir+"stations/geom_*.csv")

    # run addmMeta for the sources from getSourceObsMetaLocationType
    for index, row in df.iterrows():
        addMeta(ingestDir, inputFile[0], row['data_source'], row['source_name'], row['source_archive'], row['units'], row['location_type'])

    # remove geom file
    os.remove(inputFile[0])

    # Create list of program commands
    program_list = []
    program_list.append(['python','ingestTasks.py','--ingestDir',ingestDir,'--inputTask','ingestSourceData'])

    # Run list of program commands using subprocess
    for program in program_list:
        logger.info('Run '+" ".join(program))
        output = subprocess.run(program, shell=False, check=True)
        logger.info('Ran '+" ".join(program)+" with output returncode "+str(output.returncode))

# Main program function takes args as input, which contains the ingestDir, and outputFile values.
@logger.catch
def main(args):
    ''' Main program function takes args as input, starts logger, runs addMeta(), which writes output to CSV file.
        The CSV file will be ingest into table drf_gauge_source when ingestObsSourceData() function is run in ingestObsTask.py
        Parameters
            args: dictionary
                contains the parameters listed below
            ingestDir: string
                Directory path to the ast-run-ingester directory
            inputLocationType: string
                gauge location type (COASTAL, TIDAL, or RIVERS)
        Returns
            CSV file
    '''

    # Add logger
    logger.remove()
    log_path = os.path.join(os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs')), '')
    logger.add(log_path+'createIngestNewObsSourceMeta.log', level='DEBUG')
    logger.add(sys.stdout, level="DEBUG")
    logger.add(sys.stderr, level="ERROR")

    # Extract args variables
    ingestDir = os.path.join(args.ingestDir, '')
    inputLocationType = args.inputLocationType

    logger.info('Start processing source data for location type '+inputLocationType+'.')

    # Run addMeta function
    runIngestObsSourceData(ingestDir, inputLocationType)
    logger.info('Finished processing location type '+inputLocationType+'.')

# Run main function takes ingestDir, and outputFile as input.
if __name__ == "__main__":
    ''' Takes argparse inputs and passes theme to the main function
        Parameters
            ingestDir: string
                Directory path to the ast-run-ingester directory
            inputLocationType: string
                Gauge location type (COASTAL, TIDAL, or RIVERS)
        Returns
            None
    '''         

    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("--ingestDIR", "--ingestDir", help="Output directory path", action="store", dest="ingestDir", required=True)
    parser.add_argument("--inputLocationType", help="Input location type", action="store", dest="inputLocationType", required=True)

    # Parse input arguments
    args = parser.parse_args()

    # Run main
    main(args)
