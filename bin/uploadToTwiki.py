#!/usr/bin/env python

import wbmtools.wbmparser
import requests
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='uploads file to twiki, note it doesnt have the most robust error checking...')
    parser.add_argument("--twiki",required=True,help='twiki topic')
    parser.add_argument('--input',required=True,help='file with txt to upload')
    parser.add_argument('--force',action='store_true',help='ignores the read timeout, will mean a new twiki will be created if it does not already exist')
    parser.add_argument('--create',action='store_true',help='if the twiki doesnt exist, it creates it')
    args = parser.parse_args()
    sso = wbmtools.wbmparser.SSOSession()

    base_view_url="https://twiki.cern.ch/twiki/bin/view/CMS/"
    base_save_url="https://twiki.cern.ch/twiki/bin/save/CMS/"
    
    #get our cookies of a standard page
    data = sso.read_url(base_view_url)
    #we read it first mainly to check it exists and also to cache cookies 
    try:
        data = sso.read_url(base_view_url+args.twiki)
        if data.find("<em>The topic '{}' you are trying to access does not exist, yet.</em>".format(args.twiki))!=-1:
            if args.create:
                print "twiki {} does not exist, creating it".format(args.twiki)
            else:    
                print "twiki {} does not exist, use --create option to create it".format(args.twiki)
                raise SystemExit

    except requests.exceptions.ReadTimeout:
        print "could not read twiki",args.twiki," please check if it exists, if it does exist, twiki may be down.\n If you continue to get this message use --force"
        if not args.force:
            raise SystemExit

    with open(args.input) as f:
        text = f.read()
        sso.session.post(base_save_url+args.twiki,data={"text" : text},cookies=sso.cookies)
