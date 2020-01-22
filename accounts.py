import datetime
import time

import json

from colorama import init, Fore, Back, Style
from termcolor import colored
from requests_pkcs12 import get
import requests
import os 

import re #Regex expression 
global c
global db

import re 

# setup.py
from distutils.core import setup

env = 'proda'  
def get_token(_env,_proxyurl):  
# This is courtesy of James Owen c. April 2019 
    # open token file and check expiry
    basePath = 'C:/Tools/scripts/'
    token_filename = "" 
    token_uri = "" 
    cert = "" 
    cert_pass = ""
    if _env =='proda':
        instance = 'proda.bce'
        cert = basePath + 'credentials/ossbssTools-proda-sts.pfx'
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
        cert = basePath + 'credentials/ossbssTools-prodb-sts.pfx'
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
                print('damaged token file. getting new token...\n')
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
		
_feature_group = "NAPA_TRIAL"
allAccounts = [] 
#Token for the DVR Proxy API 

tok_dvr = get_token(env, list())

session_dvr = requests.Session()
session_dvr.headers = tok_dvr

skip = "" 
while True:
    #'https://appgw-boss.proda.bce.tv3cloud.com/oss/v1/feature-groups/NAPA_TRIAL/accounts?$top=10'
    url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/feature-groups/' + _feature_group +'/accounts?$top=10'
    if len(skip) > 0: 
        url += '&$skipToken=' + skip 

    resp = session_dvr.get(url) 
    rj = resp.json() 
    print(rj)
    try: 
        accounts = rj['accountIds']
     
    except: 
        pass
    try: 
        allAccounts.extend(accounts) 
    except: 
        pass 
    
    skip = rj['skipToken'] 
    if skip == None: 
        break 

