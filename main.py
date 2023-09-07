import time
import sys
import os

SERVERS_DIR = "/srv"
if not os.path.isdir(SERVERS_DIR):
    sys.exit("SERVERS_DIR doesn't exist or is not a directory")

def read_existing_time(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                time = int(file.read().strip())
                print(f"Read timefile, time: {time}")
                return time
            except ValueError:
                pass
    else:
        print("No timefile to read")
    return None

def clean_skipfile(timefile, skipfile):
    current_time = int(time.time())
    print(f"Current time: {current_time}")
    timefile_time = read_existing_time(timefile)
    print(f"Timefile time: {timefile_time}")

    if timefile_time is None or current_time > timefile_time:
        if os.path.exists(skipfile):
            print(f'Removing skipfile {skipfile}')
            os.remove(skipfile)
    else:
        print("No skipfiles to remove")


if __name__ == '__main__':
    while True:
        print("Cleaning skipfiles...")

        items = os.listdir(SERVERS_DIR)
        directories = [item for item in items if os.path.isdir(os.path.join(SERVERS_DIR, item))]
        if "docker-mc-orchestrator" in directories: directories.remove("docker-mc-orchestrator")
        if "docker-mc-api" in directories: directories.remove("docker-mc-api")

        for server in directories:
            server_dir = f'{SERVERS_DIR}/{server}/data'
            timefile = f'/data/{server}/timefile'
            skipfile = '.skip-stop'

            dirs = [d for d in os.listdir(server_dir) if os.path.isdir(os.path.join(server_dir,d))]
            for dir in dirs:
                file = os.path.join(server_dir, dir, skipfile)
                clean_skipfile(timefile, file)
        time.sleep(3600) # 1 hour
