#!/usr/bin/env python
# coding: utf-8

# import modules
import os
import sys
import subprocess
from loguru import logger

# Run createStationMeta.py to create station data from the original station data tables (i.e. dbo_gages_all, ndbc_stations, and noaa_stations).
# Ingesting the original station data was a step described in the README.md file.
def runCreateStations(outputDir):
    # Create list of program commands
    program_list = [['python','createStationMeta.py','--outputDir',outputDir,'--outputFile','noaa_stationdata_tidal_meta.csv'],
                    ['python','createStationMeta.py','--outputDir',outputDir,'--outputFile','ndbc_stationdata_tidal_meta.csv'],
                    ['python','createStationMeta.py','--outputDir',outputDir,'--outputFile','contrails_stationdata_coastal_meta.csv'],
                    ['python','createStationMeta.py','--outputDir',outputDir,'--outputFile','contrails_stationdata_river_meta.csv']]

    # Run list of program commands using subprocess
    for program in program_list:
        logger.info('Run '+" ".join(program))
        subprocess.call(program)
        logger.info('Ran '+" ".join(program))

# Run ingestTask.py to ingest station data create by createStationMeta.py (i.e. dbo_gages_all, ndbc_stations, and noaa_stations),
# into the drf_gauge_station table. 
def runIngestStations(inputDir, ingestDir):
    # Create list of program commands
    program_list = [['python','ingestTasks.py','--inputDir',inputDir,'--ingestDir',ingestDir,'--inputTask','IngestStation']]

    # Run list of program commands using subprocess
    for program in program_list:
        logger.info('Run '+" ".join(program))
        subprocess.call(program)
        logger.info('Ran '+" ".join(program))

# Main program function takes args as input, which contains the inputDir, outputDir, ingestDir, and inputTask values.
@logger.catch
def main():
    # Add logger
    logger.remove()
    log_path = os.path.join(os.getenv('LOG_PATH', os.path.join(os.path.dirname(__file__), 'logs')), '')
    logger.add(log_path+'runIngest.log', level='DEBUG')
    logger.add(sys.stdout, level="DEBUG")
    logger.add(sys.stderr, level="ERROR")

   
    # Check if inputDir argument exist. This argument is used in runIngestStations. 
    if args.inputDir is None:
        inputDir = ''
    elif args.inputDir is not None:
        inputDir = os.path.join(args.inputDir, '')
    else:
        sys.exit('Incorrect inputDir')

    # Check if outputDir argument exist. This argument is used in runCreateStations.
    if args.outputDir is None:
        outputDir = ''
    elif args.outputDir is not None:
        outputDir = os.path.join(args.outputDir, '')
    else:
        sys.exit('Incorrect outputDir')

    # Check if ingestDir argument exist. This argument is used in runIngestStations.
    if args.ingestDir is None:
        ingestDir = ''
    elif args.ingestDir is not None:
        ingestDir = os.path.join(args.ingestDir, '')
    else:
        sys.exit('Incorrect ingestDir')

    # Check if inputTask, and run specified task 
    if inputTask.lower() == 'createstations':
        logger.info('Run create station data.')
        runCreateStation(outputDir)
        logger.info('Ran create station data.')
    elif inputTask.lower() == 'ingeststations':
        logger.info('Run ingest station data.')
        runIngestStation(inputDir, ingestDir)
        logger.info('Ran ingest station data.')
    else:
        sys.exit('Incorrect inputTask')

# Run main function 
if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("--inputDIR", "--inputDir", help="Input directory path", action="store", dest="inputDir", required=False)
    parser.add_argument("--outputDIR", "--outputDir", help="output directory path", action="store", dest="outputDir", required=False)
    parser.add_argument("--ingestDIR", "--ingestDir", help="Ingest directory path", action="store", dest="ingestDir", required=False)
    parser.add_argument("--inputTask", help="Input task to be done", action="store", dest="inputTask", choices=['CreateStation','IngestStations'], required=True)

    # Parse arguments
    args = parser.parse_args()

    # Run main
    main(args)

