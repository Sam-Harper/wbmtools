#!/usr/bin/env python

import wbmtools.wbmparser
import requests
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='uploads file to twiki, note it doesnt have the most robust error checking...')
    parser.add_argument("--twiki",required=True,help='twiki topic')
    parser.add_argument('--output',required=True,help='file with txt to upload')
    args = parser.parse_args()
    sso = wbmtools.wbmparser.SSOSession()

    auth_url="https://twiki.cern.ch/twiki/bin/view/CMS"
    base_view_url="https://twiki.cern.ch/twiki/bin/view/CMS/{}?raw=text"
    
    #get our cookies of a standard page
    data = sso.read_url(auth_url)
    #we read it first mainly to check it exists and also to cache cookies 
    try:
        data = sso.read_url(base_view_url.format(args.twiki))
        if data.find('---+ %MAKETEXT{"Note: This topic does not exist"}%')!=-1:
            print "twiki {} does not exist, perhaps you mispelt it".format(args.twiki)
            raise SystemExit
        
        with open(args.output,'w') as f:
            for line in data:
                f.write(line.encode('ascii','replace'))


    except requests.exceptions.ReadTimeout:
        print "could not read twiki",args.twiki," please check if it exists, if it does exist, twiki may be down.\n If you continue to get this message use --force"
        if not args.force:
            raise SystemExit

    
