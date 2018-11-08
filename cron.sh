# crontab script to submit jobs to the cluster

# run by:
# */10 * * * * /users/a/r/areagan/scratch/geodb/cron.sh >> /users/a/r/areagan/scratch/geodb/cron.out 2>&1

cd /users/a/r/areagan/scratch/geodb
/gpfs1/arch/x86_64/python2.7.5/bin/python qsub.py
grep -l "delete me" geoScrape.o* | xargs rm
