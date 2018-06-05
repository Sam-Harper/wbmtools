
# -----------------------------------------------------------------------------
# Name:        cern sso website parser
# Purpose:     simple function to read the content of a cern sso protected website in python
#             
#
# Author:      Sam Harper
#
# Created:     01.08.2015
# Copyright:   (c) Sam Harper 2015
# Licence:     GPLv3
# -----------------------------------------------------------------------------
import cookielib
import os
import sys
import requests
import cern_sso


class SSOSession:
    """ Manages a cern single sign on session 

    This class authenticates the CERN single sign one (sso) system 
    allowing sso protected pages to be accessed.
    """
   
    def __init__(self):
        self._check_valid_setup()
        self.session = requests.Session()
        self.cookies = None
        
    def _check_valid_setup(self):
        cert_location = os.environ.get('REQUESTS_CA_BUNDLE')
        if cert_location == None:
            print "please set the enviroment varible REQUESTS_CA_BUNDLE to point to the location of the CERN CA certs"
            sys.exit()

        if os.path.isfile(cert_location) == False:
            print "cern ca certs location {} doesnt exist, please set REQUESTS_CA_BUNDLE to the correct location" % cookie_location
            sys.exit()

        if sys.version_info< (2,7):
            print "Warning python version is: "
            print sys.version
            print "problems have been encountered in 2.6, suggest you move to>= 2.7 (CMSSW version)"
            sys.exit()

    
    def read_url(self,url):
        if not self.cookies:
            try:
                self.cookies = cern_sso.krb_sign_on(url)
            except requests.exceptions.HTTPError as ex:
                print "error in getting kerberos cookies\n    ",ex,"\nmost likely you dont have a kerberos ticket active (or you are not allowed to view the webpage)\ntry doing a kinit\n"
                sys.exit()

        nr_tries = 0
        max_tries = 3
        while nr_tries < max_tries:
            try:
                data = self.session.get(url,cookies=self.cookies)
                nr_tries = max_tries
            except requests.exceptions.ConnectionError:
                nr_tries += 1
                print "connection error, re-trying ",nr_tries
           
        return data.text
  


