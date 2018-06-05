#!/usr/bin/env python

def convert_to_ranges(vals):
    vals.sort()
    ranges = []
    prev_val = -1
    start_val = -1
    for val in vals:
        if val - prev_val > 1:
            if prev_val != -1 :
                ranges.append(str(start_val)+"-"+str(prev_val))
            start_val = val
        prev_val = val
    
    ranges.append(str(start_val)+"-"+str(prev_val))
            
    return ranges

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()

import argparse
parser = argparse.ArgumentParser(description='prints the lumi sections in a given column ')
parser.add_argument('runs',nargs="+",help='inputFilename')
args = parser.parse_args()


for run in  args.runs:
   
    lumis_by_ps = wbmutil.get_lumis_vs_pscol(run,wbmparser)
    ps_cols = lumis_by_ps.keys();
    ps_cols.sort()
    print "run :",run
    for ps_col in ps_cols:
        if ps_col != -1: 
            print "   ",ps_col,convert_to_ranges(lumis_by_ps[ps_col])
        
    
