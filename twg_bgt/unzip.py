import zipfile
import os
import shutil
import sys
import subprocess
import time
import psutil

def is_process_running(process_name):
    """Check if there is any running process that contains the given name."""
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == process_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def wait_for_process_to_exit(process_name):
    """Wait until the specified process is no longer running."""
    print(f"Checking if {process_name} is running...")
    while is_process_running(process_name):
        print(f"{process_name} is running. Waiting...")
        time.sleep(5)  # Wait for 5 seconds before checking again.
    print(f"{process_name} is no longer running. Proceeding...")

def main():
    # Check and wait for twg.exe to exit if it's running
    twg_executable = 'twg.exe'
    wait_for_process_to_exit(twg_executable)

    # Unzip twg.zip to the current directory
    zip_filename = 'twg.zip'
    extract_dir = 'twg'

    # Check if the zip file exists
    if not os.path.isfile(zip_filename):
        print(f"Error: {zip_filename} not found!")
        return

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall()

    # Delete the zip file after extraction
    try:
        os.remove(zip_filename)
        print(f"{zip_filename} deleted.")
    except Exception as e:
        print(f"Error: Could not delete {zip_filename}. {e}")

    # Copy contents of "twg" to the current directory
    if not os.path.isdir(extract_dir):
        print(f"Error: Extracted directory {extract_dir} not found!")
        return

    for item in os.listdir(extract_dir):
        s = os.path.join(extract_dir, item)
        d = os.path.join('.', item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Run twg.exe without waiting
    if os.path.isfile(twg_executable):
        print(f"Launching {twg_executable}...")
        try:
            subprocess.Popen([twg_executable])
            print(f"{twg_executable} launched successfully.")
        except Exception as e:
            print(f"Error: Failed to launch {twg_executable}. {e}")

    # Delete the twg directory
    try:
        shutil.rmtree(extract_dir)
        print(f"{extract_dir} directory deleted.")
    except Exception as e:
        print(f"Error: Could not delete {extract_dir} directory. {e}")

    # Schedule the deletion of this script
    script_name = sys.argv[0]
    try:
        # This command schedules the script for deletion using a separate process
        subprocess.Popen(f"cmd /c del {script_name}", shell=True)
    except Exception as e:
        print(f"Error: Could not schedule deletion of the script. {e}")

if __name__ == '__main__':
    main()