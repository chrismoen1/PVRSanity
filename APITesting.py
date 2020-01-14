# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:01:31 2019

@author: Me
"""
import time 
import requests
import json
from requests_pkcs12 import get
import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.pyplot import figure
import statistics
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

def getProdCTime_DVR(env,backend): 
    top = '100'
    skipToken = ''
    
    tok_oss = get_token("DVRPROXY", env,list())
    session_oss = requests.Session() 
    session_oss.headers = tok_oss 
    

    url_recordingDefinitionsOSS= 'https://appgw-client.'+env+'.bce.tv3cloud.com/'+backend+'/dvrproxy/v1/tenants/default/accounts/napaclient40/recording-definitions/?orderby=startdate&$top='+top+'&$skipToken='+skipToken
    time_elapsed = session_oss.get(url_recordingDefinitionsOSS).elapsed.total_seconds() 
    
    return time_elapsed 

#Getting an API benchmark 
sVer = ['S96','S108','S116'] 
prodc_108 =[] 
prodc_116 =[] 
i = 0 
rang_ = [] 
#Getting an API benchmark 
prodC_116 = [] 
prodC_108 = [] 
proda = [] 
prodb = [] 
rang_ = [] 
i = 0
while (True): 
    time_prodC_116 = getProdCTime_DVR('prodc','S116')
    time_prodC_108 = getProdCTime_DVR('prodc','S108')
    time_prodA = getProdCTime_DVR('proda','S96')
    time_prodB = getProdCTime_DVR('prodb','S108')
    
    proda.append(time_prodA) 
    
    print("Prod A ", time_prodA) 
    
    prodC_116.append(time_prodC_116)
    print("Prod C 108", time_prodC_108) 
    print("Prod C 116", time_prodC_116) 
    prodC_108.append(time_prodC_108)
    prodb.append(time_prodB) 
    print("Prod B 108", time_prodB) 
    i = i + 1
    rang_.append(i)
    if i == 100: 
        break
    
    #time.sleep(0.1)
fig = plt.figure(figsize=(20,10)) 
plt.scatter(rang_,proda,c='g',label='Prod A Response Times') 
plt.scatter(rang_,prodC_116,c='b',label='Prod C R116 Response Times') 
plt.scatter(rang_,prodC_108,c='y',label='Prod C R108 Response Times') 
plt.scatter(rang_,prodb,c='r',label='Prod B R108 Response Times') 
plt.legend() 
#plt.show() 

print("Prod A Average Time " , statistics.mean(proda)) 
print("Prod B Average Time ", statistics.mean(prodb)) 
print("Prod C Average Time (R108) ", statistics.mean(prodC_108)) 
print("Prod C Average Time (R116) ", statistics.mean(prodC_116)) 

fig.savefig('finalPlot.png',dpi=fig.dpi)

