# -----------------------------------------------------------------------------
# Name:        wmb parser
# Purpose:     simple class to parse WBM webpages
#             
#
# Author:      Sam Harper
#
# Created:     12.09.2016
# Copyright:   (c) Sam Harper 2016
# Licence:     GPLv3
# -----------------------------------------------------------------------------

from cernssoparser import SSOSession
from htmlparser import HTMLTableParser

#it was noticed that if hit the server to fast, we have connection issues
#therefore we put steps in place to throttle the speed if we detect
#a Cern Authentication page
class WBMParser(SSOSession):
    """This class parses WBM pages

    This class parses WBM pages. These pages consist of tables.
    """

    def parse_url_tables(self,url):
        parser = HTMLTableParser()
        parser.feed(self.read_url(url))
        try:
            count=0
            while len(tables)<=1 and count<=10 and parser.titles[0]=="Cern Authentication":
                from time import sleep
                sleep(3)
                parser.feed(self.read_url(url))
                count+=1
                pass

        except:
            pass
        return parser.tables

    def parse_url_tables_format(self,url):
        parser = HTMLTableParser()
        parser.feed(self.read_url(url))
        try:
            count=0
            while len(tables)<=1 and count<=10 and parser.titles[0]=="Cern Authentication":
                from time import sleep
                sleep(3)
                parser.feed(self.read_url(url))
                count+=1
        except:
            pass
        return parser.tables,parser.tablesFormat

    def parse_url(self,url):
        parser = HTMLTableParser()
        parser.feed(self.read_url(url))
        try:
            count=0
            while len(tables)<=1 and count<=10 and parser.titles[0]=="Cern Authentication":
                from time import sleep
                sleep(3)
                parser.feed(self.read_url(url))
                count+=1
        except:
            pass
        return parser    
        

        
        
    

