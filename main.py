import logging
import time
import sys
import os

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

SERVERS_DIR = str(os.getenv('MC_SERVERS_DIR'))
if not os.path.isdir(SERVERS_DIR):
    sys.exit(f"SERVERS_DIR: ({SERVERS_DIR}) doesn't exist or is not a directory")

def read_existing_time(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                time = int(file.read().strip())
                logging.debug(f"Read timefile, time: {time}")
                return time
            except ValueError:
                pass
    else:
        logging.debug("No timefile to read")
    return None

def clean_skipfile(timefile, skipfile):
    current_time = int(time.time())
    logging.debug(f"Current time: {current_time}")

    timefile_time = read_existing_time(timefile)
    logging.debug(f"Timefile time: {timefile_time}")

    if timefile_time is None or current_time > timefile_time:
        if os.path.exists(skipfile):
            logging.info(f"Current time ({current_time}) is greater than timefile_time ({timefile_time})")
            logging.info(f'Removing skipfile {skipfile}')
            os.remove(skipfile)
    else:
        logging.debug("Not removing any skipfiles")


if __name__ == '__main__':
    while True:
        logging.debug("Cleaning skipfiles...")

        items = os.listdir(SERVERS_DIR)
        directories = [item for item in items if os.path.isdir(os.path.join(SERVERS_DIR, item))]

        for server in directories:
            server_dir = f'{SERVERS_DIR}/{server}/data'
            timefile = f'/data/{server}/timefile'
            skipfile = '.skip-stop'

            dirs = [d for d in os.listdir(server_dir) if os.path.isdir(os.path.join(server_dir,d))]
            for dir in dirs:
                file = os.path.join(server_dir, dir, skipfile)
                clean_skipfile(timefile, file)
        time.sleep(3600) # 1 hour
