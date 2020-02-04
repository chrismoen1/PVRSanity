
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:14:00 2019

@author: Chris Moen
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 16:37:39 2019

@author: Chris Moen
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 11:15:49 2019

@author: Chris Moen
"""
import datetime
import time
import json

from colorama import init, Fore, Back, Style
from termcolor import colored
from requests_pkcs12 import get
import requests
import os 
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import re #Regex expression 
global c
global db

import re 
# setup.py
from distutils.core import setup
counter = 0
path = "D:\\scripts\\output\\hourly_C"

class SanityData:
    def __init__(self): 
        self.valMissingIDs_program = 0 
        self.valIndRecs_program = 0
        self.valImages_program = 0
        self.valDVRIds_program = 0
        self.accountConfigurationVal_program = 0 
        self.progDetails = 0 
        self.outOfSync = 0 
        self.fake_generic = 0 
        self.originalAirDate = [] 
        self.errorCodes = [] 
        self.enableConfiguration = 0
        self.devices = 0 
        self.skipTokenError = 0 
        self.DVREmptyData = 0
        self.dvrStationOutOfSync = 0 
        self.dvr_s96 = 0 
        self.dvr_s108 = 0 
        self.dvr_s116 = 0
        self.oss = 0
    def getOriginalAirDate(self): 
        return self.originalAirDate
    def getEnableConfiguration(self): 
        return self.enableConfiguration 
    def getMissingIDS(self): 
        return self.valMissingIDs_program 
    def getValIndRecs(self): 
        return self.valIndRecs_program
    def valImages(self): 
        return self.valImages_program 
    def valDVRIds(self): 
        return self.valDVRIds_program 
    def getAccountConfigurationVal(self): 
        return self.accountConfigurationVal_program
    def getProgDetails(self): 
        return self.progDetails
    def getDVROutOfSync(self): 
        return self.outOfSync
    def getFake_generic(self): 
        return self.fake_generic
    def getDevices(self): 
        return self.devices
    def getDVREmptyData(self): 
        return self.DVREmptyData
    def getSkipTokenError(self): 
        return self.skipTokenError
    def setSkipTokenError(self,skipToken): 
        self.skipTokenError += skipToken
    def setDevices(self,devices): 
        self.devices += devices
    def errorResponseCode(self,code): 
        self.errorCodes.append(code) 
    def getErrorResponseCode(self,code): 
        return self.errorCodes
    def setEnableConfiguration(self,enableConfiguration): 
        if enableConfiguration != None: 
            self.enableConfiguration += enableConfiguration
    def setOriginalAirDate(self,originalAirDate): 
        if originalAirDate != None: 
            self.originalAirDate.append(originalAirDate) 
    def setValMissingIDS(self, valMissingIDs): 
        if valMissingIDs != None: 
            self.valMissingIDs_program += valMissingIDs
    def setValIndRecs(self,valIndRecs):
        if valIndRecs != None: 
            self.valIndRecs_program += valIndRecs
    def setValImages(self,valImages):
        if valImages != None: 
            self.valImages_program += valImages 
    def setValDVRIds(self,valDVRIds): 
        if valDVRIds != None: 
            self.valDVRIds_program += valDVRIds
    def setAccountConfigurationVal(self, accountConfigurationVal): 
        if accountConfigurationVal != None: 
            self.accountConfigurationVal_program += accountConfigurationVal
    def setProgDetails(self,progDetails): 
        if progDetails != None: 
            self.progDetails += progDetails
    def setDVROutOfSync(self,outOfSync): 
        if outOfSync != None: 
            self.outOfSync += outOfSync
    def setfake_generic(self,fake_generic): 
        if fake_generic != None: 
            self.fake_generic += fake_generic
    def setDVREmptyData(self,dvrData): 
        if dvrData != None: 
            self.DVREmptyData += dvrData 
    def setAPIResponse(self,dvr_s96,dvr_s108,dvr_s116,oss): 
        self.dvr_s96 += dvr_s96
        self.dvr_s108 += dvr_s108
        self.dvr_s116 += dvr_s116
        self.oss += oss
        
    def setdvrStationOutOfSync(self,dvrStationOutOfSync): 
        self.dvrStationOutOfSync += dvrStationOutOfSync 
    def getdvrStationOutOfSync(self): 
        return self.dvrStationOutOfSync
        
    def getDVR_S96(self): 
        return self.dvr_s96 
    def getDVR_S108(self): 
        return self.dvr_s108 
    def getDVR_s116(self): 
        return self.dvr_s116 
    def getOSS(self): 
        return self.oss
def get_token(type_cert,_env,_proxyurl):
    #This is courtesy of James Owen c. April 2019 
    # open token file and check expiry
    basePath = 'C:/Tools/scripts/'
    token_filename = "" 
    token_uri = "" 
    cert = "" 
    cert_pass = ""
    
    if _env =='proda':
        instance = 'proda.bce'
        
        if type_cert == 'OSS': 
            cert = basePath + 'credentials/ossbssTools-proda-sts.pfx'
        elif type_cert == 'DVRPROXY': 
            cert = basePath + 'credentials/ndvrTools-proda-sts.pfx'
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'
    elif _env == 'prodc':
        instance = 'prodc.bce'
        cert = basePath + 'credentials/ucpusher-ssl.pfx'
        cert_pass = ''
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'
    elif _env == 'prodb':
        instance = 'prodb.bce'
        
        if type_cert == 'OSS': 
            cert = basePath + 'credentials/ossbssTools-prodb-sts.pfx'
        elif type_cert == 'DVRPROXY': 
            cert = basePath + 'credentials/ndvrTools-prodb-sts.pfx'
            
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.'+instance+'.tv3cloud.com/certactive'
        token_filename = './'+instance+'_token.json'

    token_valid = 0
    try:
        with open(token_filename, 'r') as token_file_in:
            try:
                token = json.load(token_file_in)
                if ((datetime.datetime.timestamp(dateutil.parser.parse(token['RefreshTime'])) - time.time()) > 0 ):
                    token_valid = 1
                    # print(bcolors.OKGREEN + 'token loaded ok. proceeding...\n' + bcolors.ENDC)
                else:
                    print('token expired. getting new token...\n')
            except:
                pass
    except OSError:
        print('no token file. getting new token...\n')

    if (token_valid):
        pass
    else:
        response = get(token_uri, headers={'Content-Type': 'application/json'}, verify=True, pkcs12_filename=cert, pkcs12_password=cert_pass, proxies=_proxyurl)
        if (response.status_code == 200 ):
            token = response.json() # load token from repsonse.get()
            with open(token_filename, 'w', encoding="utf-8", newline='\n') as token_file:
                try:
                    json.dump(response.json(),token_file, indent=4, sort_keys=True, ensure_ascii=False)
                    token_file.write('\n')
                    token_file.close()
                    # print (bcolors.OKGREEN + 'token saved ok. proceeding...\n' + bcolors.ENDC)
                except OSError:
                    print(bcolors.WARNING + 'can\'t create files.  bailing...' + bcolors.ENDC + '\n')
                    sys.exit('barf!')
        else:
            print ('token request response: ', response.json()['ErrorDescription'],'\n')
            sys.exit ('invalid cert or wrong password\n')

    try:
        auth_header = { 'Authorization': 'OAUTH2 access_token="'+(token['AccessToken'])+'"', 'Content-Type': 'application/json' }
        return auth_header
    except:
        return None
 
def mf_getRecordings(typeCALL,accountName,env): 
                         
    skipToken = ""
    tok = get_token(typeCALL,env, list())
    
    session = requests.Session()
    session.headers = tok
    
    while(skipToken != None):
        
        top = str(100)
        
        if typeCALL == 'OSS': 
            url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
       
        try: 
            response = session.get(url)
            return str(response.status_code)
            #checkResponseType(response) 
        except: 
            return 
def getAccounts_FeatureGroup(_feature_group,env):
    tok = get_token('OSS',env, list())
    
    session = requests.Session()
    session.headers = tok
    
    allAccounts = [] 
    skip = "" 

    while True:
        url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/feature-groups/' + _feature_group +'/accounts?$top=10'
        if len(skip) > 0: 
            url += '&$skipToken=' + skip 

        resp = session.get(url) 
        rj = resp.json() 
        try: 
            accounts = rj['accountIds']
        except: 
            pass
        
        try: 
            allAccounts.extend(accounts)
        except: 
            pass 
        
        try: 
            skip = rj['skipToken'] 
        except: 
            break 
        if skip == None: 
            break 

    return allAccounts 

def main(): 
    
    env = 'prodc'
    sanityData = SanityData() #Class to hold    all of the sanity data 
        
    print("Accounts with 503 errors: ", env)
    
    _feature_group = "NAPA_TRIAL"

    accountsInFeatureGroup = getAccounts_FeatureGroup(_feature_group,env)    
    
    #accountsInFeatureGroup = ['napaclient9'] 
    #accountsInFeatureGroup = ['ucclient20']

    #featureGroupLen = len(accountsInFeatureGroup)
    
    for eachAccount in accountsInFeatureGroup:
        
        Response = mf_getRecordings('OSS',eachAccount,env)
        if Response == '503': 
            print(Response + " " + eachAccount)  

main() #Return the Test Results 