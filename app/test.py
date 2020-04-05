import pandas as pd
import os
import time

print os.path.isfile('myFile.txt')

#fileStatsObj = os.stat('myFile.txt')
#mod_time = time.ctime(fileStatsObj[stat.ST_MTIME])
mod_time = os.path.getmtime('myFile.txt')

print mod_time
