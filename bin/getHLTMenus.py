#!/usr/bin/env python

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()
runs=wbmutil.get_runs_from_fills("2017.08.20","2018.11.01",wbmparser)

runs.sort()
for run in  runs:
    runinfo=wbmutil.get_run_info(run,wbmparser)
    #print run,runinfo
    if runinfo!=None:
        print run,runinfo["hltMenu"]
    else:
        print run,"error not found"

    

    
