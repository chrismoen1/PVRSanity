# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:01:31 2019

@author: Me
"""
import time 
import requests
import json
from requests_pkcs12 import get
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
 

#Getting an API benchmark 
sVer = ['S96','S108','S116'] 
while (True): 
    env = 'prodc'
    top = '100'
    skipToken = ''
    
    tok_oss = get_token("DVRPROXY", env,list())
    session_oss = requests.Session() 
    session_oss.headers = tok_oss 
    
    url_recordingDefinitionsOSS= 'https://appgw-client.'+env+'.bce.tv3cloud.com/S108/dvrproxy/v1/tenants/default/accounts/ucclient20/recording-definitions/?orderby=startdate&$top='+top+'&$skipToken='+skipToken
    #url_recordingDefinitionsOSS = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/accounts/ucclient20/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
    try: 
        response = session_oss.get(url_recordingDefinitionsOSS)
    except: 
        pass
    #testSkipToken(url) 
    rj = response.json()   
    print(rj['skipToken']) 
    #@time.sleep(5)