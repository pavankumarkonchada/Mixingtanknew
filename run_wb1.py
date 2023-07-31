import subprocess
import pyautogui
import time
# Specify the path to the Workbench executable
workbench_path = r"C:\Program Files\ANSYS Inc\v222\Framework\bin\Win64\RunWB2.exe"
#Specifying the path to the workbench journal file to be executed, this needs to be like this and will be replaced with the proper value in run_wb2.py
wb_journal_path=journal_loc

# Construct the command to open the workbench with the journal
command = f'"{workbench_path}" -B -R "{wb_journal_path}"'

# Open the command created as a shell command
subprocess.Popen(command, shell=True)
