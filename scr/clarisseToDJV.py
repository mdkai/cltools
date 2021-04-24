# Runs the latest blast using the djv player.
# It looks for the latest PNG sequence in the temp folder.

rvPlay = "/mnt/pipeline/software/TweakSoftware/Linux/RV-7.3.0-x64/bin/rv"
sequenceFormat = "png"

import glob
import os
import subprocess
import tempfile

path = tempfile.gettempdir() # gets the current temporary directory
#list_of_files = glob.glob(path + '/*.' + sequenceFormat) # list all the files inside the temp folder
#latest_file = max(list_of_files, key=os.path.getctime) # gets the last file

seq = path +'/'+ 'blast.' + '%04d.' +sequenceFormat


subprocess.call([rvPlay, seq, '-play', '-c']) # runs the player