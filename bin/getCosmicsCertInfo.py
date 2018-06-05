#!/usr/bin/env python
import sys
import math
from termcolor import colored


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


def make_inc_subsys_str(inc_subsys):
    sub_systems=["CSC","CTPPS","CTPPS_TOT","DAQ","DCS","DQM","DT","ECAL","ES","HCAL","HF","PIXEL","RPC","SCAL","TCDS","TRACKER","TRG"]
    subsys_str=""
    for sub_sys in sub_systems:

        colour = 'red'
        if sub_sys in inc_subsys:
            colour = 'green'
        subsys_str += colored(sub_sys,colour)+" "
            
    return subsys_str


import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()
#runs=wbmutil.get_runs_from_fills("2016.01.01","2017.01.01",parser)

import argparse
parser = argparse.ArgumentParser(description='prints the lumi sections in a given column ')
parser.add_argument('runs',nargs="+",help='inputFilename')
parser.add_argument('-w','--width',help='Number of columns to print per iteration',type=int,default=10)
args = parser.parse_args()


sub_systems=["CSC","CTPPS","CTPPS_TOT","DAQ","DCS","DQM","DT","ECAL","ES","HCAL","HF","PIXEL","RPC","SCAL","TCDS","TRACKER","TRG"]

for run in args.runs:
    runinfo=wbmutil.get_run_info(run,wbmparser)
    lumis_by_ps = wbmutil.get_lumis_vs_pscol(run,wbmparser)
    ps_cols = lumis_by_ps.keys();
    ps_cols.sort()
    ps_col_str = ""
    for ps_col in ps_cols:
        if ps_col != -1: 
            ls_ranges=convert_to_ranges(lumis_by_ps[ps_col])
            ps_col_str += str(ps_col)+":"
            for ls_range in ls_ranges:
                ps_col_str+="["+ls_range+"],"
    ps_col_str=ps_col_str[:-1]

   
    #print run,runinfo
    if runinfo!=None:
        included_subsys = make_inc_subsys_str(runinfo["components"])
        print run,runinfo["hltMenu"],included_subsys,ps_col_str#runinfo["components"]
    else:
        print run,"error not found"
        

path_names=["HLT_CaloJet10_NoJetID_HCALPhase1","HLT_CaloJet10_NoJetID","HLT_CaloJet20_NoJetID_HCALPhase1","HLT_CaloJet20_NoJetID","HLT_CaloJet500_NoJetID","HLT_CaloJet50_NoJetID_HCALPhase1","HLT_CaloJet50_NoJetID","HLT_HT200","HLT_L1DoubleIsoTau32er","HLT_L1DoubleJetC50","HLT_L1DoubleMu0","HLT_L1SingleEG10","HLT_L1SingleEG18","HLT_L1SingleEG5","HLT_L1SingleJet200","HLT_L1SingleJet35","HLT_L1SingleMu3","HLT_L1SingleMu5","HLT_L1SingleMu7","HLT_L1SingleMuCosmics","HLT_L1SingleMuOpen_DT","HLT_L1SingleMuOpen","HLT_L2DoubleMu23_NoVertex","HLT_L2Mu10_NoVertex_NoBPTX3BX","HLT_L2Mu10_NoVertex_NoBPTX","HLT_L2Mu40_NoVertex_3Sta_NoBPTX3BX","HLT_L2Mu45_NoVertex_3Sta_NoBPTX3BX","HLT_Photon22","HLT_UncorrectedJetE30_NoBPTX3BX","HLT_UncorrectedJetE30_NoBPTX","HLT_UncorrectedJetE60_NoBPTX3BX","HLT_UncorrectedJetE70_NoBPTX3BX"]

width = args.width
count = 0
run_list = args.runs[count*width:(count+1)*width]
while len(run_list) > 0:
    path_rates = {}
    for path in path_names:
        path_rates[path] = []

    sys.stdout.write("\nGetting rates")
    for index,run in enumerate(run_list):
        if index % 3 == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
        hlt_rates = wbmutil.get_hlt_rates(run,wbmparser)
        if hlt_rates != None:
            for hlt_path in path_rates:
                try:
                    path_rates[hlt_path].append(hlt_rates[hlt_path])
                except KeyError:
                    path_rates[hlt_path].append("-1")
    print "\n"
    max_path_length = 0
    for hlt_path in path_rates.keys():
        if len(hlt_path) > max_path_length:
            max_path_length = len(hlt_path)

    print_str = '{:'+ str(max_path_length) + '} '
    for run in run_list:
        print_str += '{:^8} '

    print print_str.format("name",*run_list)
    for hlt_path in sorted(path_rates.keys()):
        print print_str.format(hlt_path,*path_rates[hlt_path])

    count += 1
    run_list = args.runs[count*width:(count+1)*width]


