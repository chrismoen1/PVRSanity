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
oo
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

import re  # Regex expression

global c
global db

import re
# setup.py
from distutils.core import setup


path = "D:\\scripts\\output\\hourly_C"
total = 0

list_week= [0,0]
list_month = [0,0]
list_6month = [0,0]
list_year = [0,0]

def get_token(type_cert, _env, _proxyurl):
    # This is courtesy of James Owen c. April 2019
    # open token file and check expiry
    basePath = 'C:/Tools/scripts/'
    token_filename = ""
    token_uri = ""
    cert = ""
    cert_pass = ""

    if _env == 'proda':
        instance = 'proda.bce'

        if type_cert == 'OSS':
            cert = basePath + 'credentials/ossbssTools-proda-sts.pfx'
        elif type_cert == 'DVRPROXY':
            cert = basePath + 'credentials/ndvrTools-proda-sts.pfx'
        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'


    elif _env == 'prodc':
        instance = 'prodc.bce'
        cert = basePath + 'credentials/ucpusher-ssl.pfx'
        cert_pass = ''
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'
    elif _env == 'prodb':
        instance = 'prodb.bce'

        if type_cert == 'OSS':
            cert = basePath + 'credentials/ossbssTools-prodb-sts.pfx'
        elif type_cert == 'DVRPROXY':
            cert = basePath + 'credentials/ndvrTools-prodb-sts.pfx'

        cert_pass = 'Medi@F1rst'
        token_uri = 'https://appgw-operatorstsssl.' + instance + '.tv3cloud.com/certactive'
        token_filename = './' + instance + '_token.json'

    token_valid = 0
    try:
        with open(token_filename, 'r') as token_file_in:
            try:
                token = json.load(token_file_in)
                if ((datetime.datetime.timestamp(dateutil.parser.parse(token['RefreshTime'])) - time.time()) > 0):
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
        response = get(token_uri, headers={'Content-Type': 'application/json'}, verify=True, pkcs12_filename=cert,
                       pkcs12_password=cert_pass, proxies=_proxyurl)
        if (response.status_code == 200):
            token = response.json()  # load token from repsonse.get()
            with open(token_filename, 'w', encoding="utf-8", newline='\n') as token_file:
                try:
                    json.dump(response.json(), token_file, indent=4, sort_keys=True, ensure_ascii=False)
                    token_file.write('\n')
                    token_file.close()
                    # print (bcolors.OKGREEN + 'token saved ok. proceeding...\n' + bcolors.ENDC)
                except OSError:
                    print(bcolors.WARNING + 'can\'t create files.  bailing...' + bcolors.ENDC + '\n')
                    sys.exit('barf!')
        else:
            print('token request response: ', response.json()['ErrorDescription'], '\n')
            sys.exit('invalid cert or wrong password\n')

    try:
        auth_header = {'Authorization': 'OAUTH2 access_token="' + (token['AccessToken']) + '"',
                       'Content-Type': 'application/json'}
        return auth_header
    except:
        return None

    # THen we kno


def timeDelta(time1, time2):  # time stamp

    time1_st = datetime.datetime.strptime(time1, "%Y-%m-%dT%H:%M:%SZ")
    time2_st = datetime.datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")

    delta = time2_st - time1_st
    delta_seconds = delta.total_seconds()
    # If the delta time is negative, then we know that it was scheduled in the past
    return delta_seconds / (24 * 60 * 60)

def chooseBucket(startUTC, genres, ratings,accountName,show,state, glfProgram,name,description):
    #This will choose the appropriate bucket

    '''
    list_week= [0,0]
    list_month = [0,0]
    list_6month = [0,0]
    list_year = [0,0]

    '''

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', 'T') + 'Z'
    delta = timeDelta(startUTC, time_now)
    if delta < 7:
        #Less than 7 days
        if ratings == "No Ratings" or genres == "No Genres":
            list_week[0] += 1
            print("Last 7 Days ..............")
            print("Account Name ", accountName)
            print("GLF Program ID", glfProgram)
            print("Program Name ", name)

            print("Description ",description )
            print("Rating ", ratings)

            print("Genres ", genres)
            print("Show Name", show)
            print("State: ", state)
            print(" -------------------------------------------- ")

        else:
            list_week[1] += 1

    elif delta >= 7 and delta <= 37:

        # Less than 7 days
        if ratings == "No Ratings" or genres == "No Genres":
            list_month[0] += 1
            #print("Account Name ", accountName)

            print("Last 30 Days ..............")
            print("Account Name ", accountName)
            print("GLF Program ID", glfProgram)
            print("Program Name ", name)

            print("Description ", description)
            print("Rating ", ratings)

            print("Genres ", genres)
            print("Show Name", show)
            print("State: ", state)
            print(" -------------------------------------------- ")
        else:
            list_month[1] += 1

    elif delta <= (6 * 30) and delta > 37:

        if ratings == "No Ratings" or genres == "No Genres":
            list_6month[0] += 1
            print("Last 6 months ..............")
            print("Account Name ", accountName)
            print("GLF Program ID", glfProgram)
            print("Program Name ", name)

            print("Description ", description)
            print("Rating ", ratings)

            print("Genres ", genres)
            print("Show Name", show)
            print("State: ", state)
            print(" -------------------------------------------- ")
        else:
            list_6month[1] += 1

    else:
        if ratings == "No Ratings" or genres == "No Genres":
            list_year[0] += 1
            print("Last year ..............")
            print("Account Name ", accountName)
            print("GLF Program ID", glfProgram)
            print("Program Name ", name)

            print("Description ", description)
            print("Rating ", ratings)

            print("Genres ", genres)
            print("Show Name", show)
            print("State: ", state)
            print(" -------------------------------------------- ")
        else:
            list_year[1] += 1
def chooseBucket_nullRecordings(seriesNameValue, startUTC, accountName):
    # This will choose the appropriate bucket

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(' ', 'T') + 'Z'
    delta = timeDelta(startUTC, time_now)
    if delta < 7:
        # Less than 7 days
        if seriesNameValue == "* ERROR * NULL Recordings Object":
            print("Account Empty (last 7 days) : ", accountName)
            list_week[0] += 1
        else:
            list_week[1] += 1
    elif delta >= 7 and delta <= 37:
        if seriesNameValue == "* ERROR * NULL Recordings Object":
            print("Account Empty (last month) ", accountName)
            list_month[0] += 1
        else:
            list_month[1] += 1

    elif delta <= (6 * 30) and delta > 37:
        if seriesNameValue == "* ERROR * NULL Recordings Object":
            print("Account Empty (last 6 months) ", accountName)
            list_6month[0] += 1
        else:
            list_6month[1] += 1

    else:
        if seriesNameValue == "* ERROR * NULL Recordings Object":
            print("Account Empty (last year) ", accountName)
            list_year[0] += 1
        else:
            list_year[1] += 1

def mf_getRecordings(typeCALL, accountName, env, DVRVersion,counter):

    tok = get_token(typeCALL, env, list())

    session = requests.Session()
    session.headers = tok
    skipToken = ""
    while (skipToken != None):

        top = str(100)

        if typeCALL == 'OSS':
            url = 'https://appgw-boss.' + env + '.bce.tv3cloud.com/oss/v1/accounts/' + accountName + '/recording-definitions/?$top=' + top + '&$skipToken=' + skipToken

        elif typeCALL == 'DVRPROXY':
            # url = 'https://appgw-client.'+env+'.bce.tv3cloud.com/S96/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?$top='+top+'&$skipToken=' + skipToken
            url = 'https://appgw-client.' + env + '.bce.tv3cloud.com/' + DVRVersion + '/dvrproxy/v1/tenants/default/accounts/' + accountName + '/recording-definitions/?orderby=startdate&$top=' + top + '&$skipToken=' + skipToken

        try:
            response = session.get(url)
            if str(response.status_code) == "503":
                print("503 Error on this account ", accountName)
                # checkResponseType(response)
        except:
            return
            # testSkipToken(url)
        rj = response.json()

        if rj == None:
            return  # Then there is nothing in this json (i.e empty )
        try:
            code = rj['code']
            if code == 'NotFound':
                return
        except:
            pass

        try:
            skipToken = rj['skipToken']
        except:

            skipToken = None
        try:
            recs = rj['recordingDefinitions']
        except:
            return


        for eachRec in recs:

            recGroup = eachRec['recordings']
            try:
                seriesDetails = eachRec['seriesDetails']
            except:
                seriesDetails = None

            if seriesDetails != None:
                seriesDetailObj = eachRec['seriesDetails']
            try:
                seriesNameObj = seriesDetailObj['name']
            except:
                seriesNameObj = None
            try:
                glfStationId = eachRec['stationId']
            except:
                glfStationId = ""

            try:
                seriesExtID = seriesDetailObj['id']
            except:
                seriesExtID = "NULL"

            try:
                seriesNameValue = seriesNameObj[0]['value']
            except:
                seriesNameValue = None

            if seriesNameValue == None or seriesNameValue == "":
                seriesNameValue = "NULL"
                # i am getting the show name from the 1st recObj in the resulting array of json objects.
                try:  # if the series object has no recording object, parsing the array will fail - catching this exception.
                    progDetail = recGroup[0]['programDetails']
                    seriesNameValue = "* " + progDetail['name']
                except:
                    seriesNameValue = "* ERROR * NULL Recordings Object"

            showName = seriesNameValue
            channelNumber = eachRec['channelNumber']
            seriesObjType = eachRec['type']

            if (recGroup != None):
                for eachRecGroup in recGroup:
                    innerRow = {}
                    try:
                        seriesID = str(eachRecGroup['id'])
                    except:
                        seriesID = "NULL"
                    try:
                        seriesObjState = str(eachRecGroup['state'])
                    except:
                        seriesObjState = "NULL"
                    try:
                        seasonNumber = str(eachRecGroup['programDetails']['seasonNumber'])
                    except:
                        seasonNumber = "NULL"
                    try:
                        epNumber = str(eachRecGroup['programDetails']['episodeNumber'])
                    except:
                        epNumber = "NULL"
                    try:
                        startUTC = str(eachRecGroup['scheduledStartUtc'])

                    except:
                        startUTC = "NULL"

                    try:
                        programDetailsGLF = programDetailsGLF = str(eachRecGroup['programDetails']['glfProgramId'])
                    except:
                        programDetailsGLF = "NULL"
                    try:
                        programDetailsID = str(eachRecGroup['programDetails']['id'])
                    except:
                        programDetailsID = "NULL"
                    try:
                        originalAirDate = eachRecGroup['programDetails']['originalAirDateTime']
                    except:
                        originalAirDate = "NULL"
                    try:
                        programDetailsGeneric = eachRecGroup['programDetails']['isGeneric']
                    except:
                        programDetailsGeneric = "NULL"
                    try:
                        externalId = eachRecGroup['externalId']
                    except:
                        externalId = "NULL"
                    try:
                        ratings = eachRecGroup['programDetails']['ratings']
                    except:
                        ratings = "No Ratings"
                    try:
                        genres = eachRecGroup['programDetails']['genres']
                    except:
                        genres= "No Genres"
                    try:
                        assetName = eachRecGroup['programDetails']['name']
                    except:
                        assetName = "No Asset Name"
                    try:
                        description = eachRecGroup['programDetails']['description']
                    except:
                        description = "No Description"

                    #print(startUTC)
                    #glfProgram, name, description,rating

                    #chooseBucket(startUTC,genres, ratings,accountName,showName,seriesObjState,programDetailsGLF,assetName,description)

                    counter += 1
                    chooseBucket_nullRecordings(seriesNameValue, startUTC, accountName)
                    # checkValidation(seriesDetailObj,accountName)
                    innerRow['Time'] = startUTC
                    innerRow['Show'] = showName
                    innerRow['Season Number'] = seasonNumber
                    innerRow['Ep'] = epNumber
                    innerRow['externalID'] = externalId
                    innerRow['Channel Number'] = channelNumber
                    innerRow['Series State'] = seriesObjState
                    innerRow['seriesObjType'] = seriesObjType
                    innerRow['programDetailsGLF'] = programDetailsGLF
                    innerRow['isGeneric'] = programDetailsGeneric
                    innerRow['glfProgramId'] = programDetailsID
                    innerRow['seriesID'] = seriesID
                    innerRow['seriesExtID'] = seriesExtID
                    innerRow['originalAirDate'] = originalAirDate
                    innerRow['recordingID'] = eachRecGroup['id']
                    innerRow['glfStationID'] = glfStationId

        if skipToken == None or skipToken == "":
            break
    # checkCatalogue(individualRecordings,tok,env)
    # print(len(individualRecordings))

def getAccounts_FeatureGroup(_feature_group, env):
    tok = get_token('OSS', env, list())

    session = requests.Session()
    session.headers = tok

    allAccounts = []
    skip = ""

    while True:
        url = 'https://appgw-boss.' + env + '.bce.tv3cloud.com/oss/v1/feature-groups/' + _feature_group + '/accounts?$top=10'

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


def main(counter):
    testResults = []
    envs = ['prodc']

    for env in envs:

        if env == 'proda':
            DVRVersion = "S96"
        elif env == 'prodb':
            DVRVersion = "S108"
        elif env == 'prodc':
            DVRVersion = "S116"

        print("Running test cases for", env)

        _feature_group = "NAPA_TRIAL"

        accountsInFeatureGroup = getAccounts_FeatureGroup(_feature_group, env)

        featureGroupLen = len(accountsInFeatureGroup)

        for eachAccount in accountsInFeatureGroup:

            try:
                mf_getRecordings('DVRPROXY', eachAccount, env, DVRVersion,counter)
            except:
                pass

counter = 0
main(counter)  # Return the Test Results


print("Since the Last 7 Days... Invalid: " + str(list_week[0]) + " and Valid: " + str(list_week[1]))
print("Since the Last month ... Invalid: " + str(list_month[0]) + " and Valid: " + str(list_month[1]))
print("Since the Last 6 months... Invalid: " + str(list_6month[0]) + " and Valid: " + str(list_6month[1]))
print("Since the Last year... Invalid: " + str(list_year[0]) + " and Valid: " + str(list_year[1]))
print("---------------------------------------------------------------------------------------")
print("Total: ", counter)