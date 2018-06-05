

from wbmparser import WBMParser

wbmbase_url="http://cmswbm.cern.ch"

 
def rm_hlt_path_version(name):
    ver_pos=name.rfind("_v")
    if ver_pos != -1:
        return str(name[:ver_pos])
    else:
        return str(name)

def get_hltprescales(triggermode,parser):   
    url=wbmbase_url+"/cmsdb/servlet/TriggerMode?KEY=%s" % triggermode
    tables=parser.parse_url_tables(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        tables=parser.parse_url_tables(url)
        count+=1
    try:
        #now a little fixing for an error in lines 2 and 3
        #tables[1][1].append('L1 Prerequisite')
        #tables[1][2][0] = '0'
        return tables[2]
    except IndexError:
        print "get_hltprescales failed for runnr",runnr
        return None

def get_hltsummary(runnr,parser):   
    url=wbmbase_url+"/cmsdb/servlet/HLTSummary?RUN=%s" % runnr
    tables=parser.parse_url_tables(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        tables=parser.parse_url_tables(url)
        count+=1
    try:
        #now a little fixing for an error in lines 2 and 3
        #tables[1][1].append('L1 Prerequisite')
        #tables[1][2][0] = '0'
        return tables[1]
    except IndexError:
        print " get_hltsummary failed for runnr",runnr
        return None
    
def get_hlt_rates(runnr,parser):
    blacklist=["Name","HLTriggerFinalPath","HLTTriggerFirstPath"]
    hltsum = get_hltsummary(runnr,parser)
    hlt_rates={}
    for entry in hltsum:
#        print runnr,entry
        try:
            path_name = rm_hlt_path_version(entry[1].split()[0])
            
            if path_name in blacklist:
                continue;
            hlt_rates[path_name]=str(entry[6])
        except IndexError:
            pass
    return hlt_rates


def get_run_info(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/RunSummary?RUN=%s" % runnr
    tables=parser.parse_url_tables(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        tables=parser.parse_url_tables(url)
        count+=1
    
    try:
        tables[1]
    except IndexError:
        print "get_run_info failed for runnr",runnr
        return None

    run_info={}
    run_data=tables[1][1]
    run_info["runnr"]=run_data[0]
    run_info["lumi"]=run_data[1]
    run_info["trigKey"]=run_data[3]
    run_info["l1Key"]=run_data[4]
    run_info["hltMenu"]=run_data[5]
    run_info["start"]=run_data[6]
    run_info["end"]=run_data[7]
    run_info["nrTriggers"]=run_data[8]
    run_info["bField"]=run_data[9]
    run_info["tier0"]=run_data[10]
    run_info["components"]=run_data[11]
    
    #this may not actually be filled for some runs
    try:
        run_data_more = tables[3]
        run_info["l1Menu"] = run_data_more[5][1]
        run_info["cmsswVersion"] = run_data_more[7][1]
        run_info["fill"] = run_data_more[14][1]
    except IndexError:
        run_info["l1Menu"] = "null"
        run_info["cmsswVersion"] = "null"
        run_info["fill"] = "-1"
    return run_info

def get_lumi_summary(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/LumiSections?RUN=%s" % runnr
    tables=parser.parse_url_tables(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        tables=parser.parse_url_tables(url)
        count+=1
    
    try:
        #fixing up the summary
        tables[1].insert(1,tables[1][0][41:])
        tables[1][0] = tables[1][0][:41]
        return tables[1]
    except IndexError:
        print "get_lumi_summary failed for runnr",runnr
        return None

def get_pscol_vs_lumisec(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/LumiSections?RUN=%s" % runnr 
    tables=parser.parse_url_tables(url)

    psAndInstLumis={}
   # print tables[0]
    for line in tables[1]:
        offset=0
        if line[0]=="L S": offset=41
        print line
        lumiSec=int(line[0+offset])
        preScaleColumn=int(line[1+offset])
#        instLumi=float(line[3+offset])
        print lumiSec,preScaleColumn
        psAndInstLumis[lumiSec]=preScaleColumn#,instLumi)
    return psAndInstLumis

def get_lumis_vs_pscol(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/LumiSections?RUN=%s" % runnr 
    tables=parser.parse_url_tables(url)

    lumis_by_ps={}
   # print tables[0]
    for line in tables[1]:
        offset=0
        if line[0]=="L S": offset=41
#        print line
        lumi_sec=int(line[0+offset])
        ps_col=int(line[1+offset])
        if ps_col not in lumis_by_ps:
            lumis_by_ps[ps_col]=[]
        lumis_by_ps[ps_col].append(lumi_sec)
#        instLumi=float(line[3+offset])
 #       print lumiSec,preScaleColumn
  #      psAndInstLumis[lumiSec]=preScaleColumn#,instLumi)
    return lumis_by_ps



def get_ave_inst_lumi(psAndInstLumis,minLS,maxLS):
    lumiSum=0.;
    nrLumis=0;
    if maxLS==-1: maxLS=max(psAndInstLumis.keys())
    for lumi in range(minLS,maxLS+1):
        if lumi in psAndInstLumis:
            nrLumis+=1
            lumiSum+=psAndInstLumis[lumi][1]
    if nrLumis!=0: return lumiSum/nrLumis
    else: return 0


def getHLTRates(runnr,minLS,maxLS):
    url=wbmbase_url+"/cmsdb/servlet/HLTSummary?fromLS=%s&toLS=%s&RUN=%s" % (minLS,maxLS,runnr)
    tables=parseURLTables(url)


    hltRates={}
    for line in tables[1][2:]:
        rates=[]
#        print line
        for entry in line[3:7]:
            rates.append(float(entry.replace(",","")))
                        
        hltRates[line[1].split("_v")[0]]=rates
        
    return hltRates


def get_runs_from_fills(start_date,end_date,wbmparser):
    url=wbmbase_url+"/cmsdb/servlet/FillSummary?runtimeTypeID=&fromTime=%s&toTime=%s&nameExp=LHCFILL&debug=0&showSection=0" % (start_date,end_date)
    tables=wbmparser.parse_url_tables(url)
    runs=[]
    for table in tables:
        if table[0][0]=="Name":
            #print table
            for line in table[1:]:
                fill_runs=line[13]
              #  print line
                for run in fill_runs.split():
                    runs.append(run)
    return runs

def get_runs_from_fill(fillnr,wbmparser):
    url=wbmbase_url+"/cmsdb/servlet/FillRuntimeChart?lhcFillID=%s" % (fillnr)
    tables=wbmparser.parse_url_tables(url)
    runs=[]
    for table in tables:
        if table[0][0]=="LHC Fill":
#            return table[1][1].split()
            return [s.encode('ascii') for s in table[1][1].split()]
            


def get_hlt_prescale_columns(l1_hlt_mode,parser):
    
    url=wbmbase_url+"/cmsdb/servlet/TriggerMode?KEY=%s" % l1_hlt_mode
    hlt_ps={}

    tables=parser.parse_url_tables(url)
    hlt_paths=tables[2]
    for line in hlt_paths:
        name = rm_hlt_path_version(line[1].split()[0])
        hlt_ps[name]=line[2:-1]
       
    return hlt_ps


def get_prescale_set(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/PrescaleSets?RUN=%s" % runnr
    tables=parser.parse_url_tables(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        from time import sleep
        sleep(3)
        tables=parser.parse_url_tables(url)
        count+=1
    
    try:
        tables[1]
        return tables[1]
    except IndexError:
        #print parser.read_url(url)
        print "get_prescale_set failed for runnr",runnr
        #import sys
        #sys.exit(0)
    
    return []

def get_prescale_set_with_mask(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/PrescaleSets?RUN=%s" % runnr
    tables,format=parser.parse_url_tables_format(url)
    
    count=0
    while len(tables)<=1 and count<=10:
        from time import sleep
        sleep(3)
        tables,format=parser.parse_url_tables_format(url)
        count+=1
    
    try:
        tables[1]
        ps_mask = map(lambda x,y:(x,y[0]),tables[1],format[1])
        return ps_mask
    except IndexError:
        #print parser.read_url(url)
        print "get_prescale_set_with_mask failed for runnr",runnr
        #import sys
        #sys.exit(0)
    
    return []

def get_dcs_by_lumi(runnr,parser):
    url=wbmbase_url+"/cmsdb/servlet/LumiSections?RUN=%s" % runnr 
    tables,tbl_format=parser.parse_url_tables_format(url)
    for index,entry in enumerate(tables[1]):
        print entry,tbl_format[1][index]

