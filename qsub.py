# accept a timestamp
# read the current date
# pump out a qsub script named by the timestamp, for the current date

import datetime
import sys
import subprocess
import time
from os.path import isdir,isfile
from os import mkdir
jobs = int(subprocess.check_output("showq | grep areagan | wc -l",shell=True))
print(jobs)

max_jobs = 150
jobs_remaining = max_jobs - jobs

loop_counter = 0
now = datetime.datetime.now()
date = datetime.datetime(now.year,now.month,now.day,now.hour-3,0)

while jobs_remaining > 0:
    if not isdir(date.strftime("zipped-raw/%Y-%m-%d")):
        mkdir(date.strftime("zipped-raw/%Y-%m-%d"))
    if not isfile(date.strftime("zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.gz")):
        # touch it
        open(date.strftime("zipped-raw/%Y-%m-%d/%Y-%m-%d-%H-%M.gz"),"a").close()
        jobs_remaining-=1
        job="""#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:30:00
#PBS -N geoScrape
#PBS -j oe

cd /users/a/r/areagan/scratch/geodb
export PATH=/users/a/r/areagan/usr/bin:$PATH

touch zipped-raw/{0}/{0}-{1}.gz
gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-{1}.gz | jq -c '\\''. | select(.geo!=null or .coordinates!=null)'\\'' | gzip > zipped-raw/{0}/{0}-{1}.gz

echo "delete me\"""".format(date.strftime("%Y-%m-%d"),date.strftime("%H-%M"))

        # print(job)
        subprocess.call("echo '{0}' | qsub -qshortq".format(job),shell=True)
        time.sleep(0.1)
    date-=datetime.timedelta(minutes=15)
    if date < datetime.datetime(2008,9,8):
        break








