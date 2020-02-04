## Brad Arsenault - c.2019
## 	brad.arsenault@bell.ca // 613-785-1583
## Calling convention: py glfaudit_stage3d.py <env> <date> <past_table>
##
##

import csv  # for bugs list
import xml.etree.ElementTree as ET
import re  # regular expressions... want re.findall(pattern,string)
import datetime
import time
import json
import sys
import dateutil.parser
from colorama import init, Fore, Back, Style
from termcolor import colored
from requests_pkcs12 import get
import pickle
import requests
import signal
from os import listdir
from os.path import isfile, join
import signal
import multiprocessing as mp
import logging
import os

session = requests.Session()
match_op = False
# requests.adapters.DEFAULT_RETRIES = 1


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


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


def mf_get_guide_poster(_pid, _env):
    env = str(_env)
    url = "https://appgw-client-a." + env + ".bce.tv3cloud.com/S96/discovery/v3/live-series/1000/" + str(
        _pid) + "/Poster/small/4x3"
    if env == "prodc":
        url = "https://appgw-client-a.prodc.bce.tv3cloud.com/S116/discovery/v3/live-series/1002/" + str(
            _pid) + "/Poster/small/4x3"
    try:
        response = session.head(url)
        code = response.status_code
    except:
        code = -1
    return code


def mf_map_program(pid, token, _env):
    url = "https://appgw-client-a." + _env + ".bce.tv3cloud.com/S96/discovery/v3/live-programs-mapper/1000/" + str(pid)
    if (_env == "prodc"):
        url = "https://appgw-client-a.prodc.bce.tv3cloud.com/S116/discovery/v3/live-programs-mapper/1002/" + str(pid)
    # print('==> Mapping program: ' + str(pid) +'\n')
    # print(url)
    try:
        response = session.get(url)  # , headers=token
        id = response.json()['Id']
        return id
    except:
        return "Error"


def get_mf_image_status(_url, _filename=None, _env=None):
    # modified Jan 16, 2020
    # modified to download image and save it to a directory.  Filename is (UID)-(filename).jpg
    if _filename == None or _env==None:
        response = session.head(_url)
    else:
        filename = os.getcwd()+"\\"+str(_env)+"\\"+str(_filename)
        response = session.get(_url, stream=True)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        output = open(filename,"wb")
        output.write(response.raw.read())
        output.close()
    code = response.status_code
    return code


def decode_tms(s):
    try:
        i = s.find("ThirdParty")
        if (i == -1):
            return s
        s = s[i + len("ThirdParty"):len(s)].lower()
    except:
        return "Error"
    f = s.find("_")
    if (f != -1):
        s = s[0:f]
    try:
        inferred_tms_id = bytes.fromhex(s).decode('utf-8')
        return inferred_tms_id
    except:
        return s
    return 0


def ret_chars(s):
    return "".join(str(s).split())


pop_s = requests.Session()
pop_s.headers = {
    "Host": "operatorportal.prodc.bce.tv3cloud.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
    # "access-token": "AuthToken1tVNdk-ooEP0144tVVkIIkAcfokZ3nOh4NU5G3zDBiBKIQPyYX3-Zrbm7Vfv54lRRTdKnOU2fbuK25EwWrH-wtjFPQfwExm5pJu5cVg3V9t5rtCqL3q5gPXsJCqHasleo2kV1no1pmf7LWWPNfxz5jP0ztDiwmprerRZG0aandOW8V-MM8LzQbb8bXjJpub27z0JQXn_iktasDyAMfM9DPgUhBHuP-ZjsfB96hR8V-wB3loyKui_4hfGykzFJpX0u-yXb01bYTiyEurLyl9_8AawN0y7uf-n_RkCF-OcKa15oZdTefunwq0byWSP6lxq1EqxPjWG2W1NJK6YfTV4oaR30bfStsapmumvaplHaPpp_z6htNbOqqgRzPbvwgj06h3sGzNiuk0c-_P7cqa8lFd2vCrqs5FY9vA2f89-lZc0lN1bTb8igGvYtvF89_d7Lm3ZnCs13bv7j1h6U5h_UciVn1Jz6IYBe4IchCjwUIQii0IcERx6MIP…gAjyH4jDwcSe5NVwz8yr7fogAwsTHoDPUbpJZ-eUMIx875-uXqJk6MbnilXSjOGTaZoe23jXaDU8fgRiNBgT7QYIGJIgSMh7DmITeCIHBKAzhOCIeGjiuRbKMs9fl6nkyj7P1MunbcqJ-u4cf2f0E8Nt4Ws4W1-V7ukTxaBrEQJGAtNt33_5YbJ1Qb5kzqxdncJ4e1-dokmzhfg6eozRV3mK3GSzvq6kW4-EWeC5qZ9Vwg-c8mTi9B84xRw1ncTss2dA760leIUQyr3XgIb1cmpc8V5H7wdMWue4Nqs20SJGMVgTDolov4EvKGRGHdTMT_hnHp7d3dg8ug9n82rhWt0WLT4J71XV9_Mh_0CHyYhF4iWM659FReTMC3g5y-l4Q8Go4PGenQ-6fc7mojWpT23ysb_yGpudqdQWjOq844qhIi8kxjthHlg_hdXbO-KsURtwS_wbxBjaOfEs3ZNae8oNcLyv_SMok3O5PrtwECg3yME1wlGbb6_UpGLn1Ew",
    # "oauth": "AuthToken1tVNdk-ooEP0144tVVkIIkAcfokZ3nOh4NU5G3zDBiBKIQPyYX3-Zrbm7Vfv54lRRTdKnOU2fbuK25EwWrH-wtjFPQfwExm5pJu5cVg3V9t5rtCqL3q5gPXsJCqHasleo2kV1no1pmf7LWWPNfxz5jP0ztDiwmprerRZG0aandOW8V-MM8LzQbb8bXjJpub27z0JQXn_iktasDyAMfM9DPgUhBHuP-ZjsfB96hR8V-wB3loyKui_4hfGykzFJpX0u-yXb01bYTiyEurLyl9_8AawN0y7uf-n_RkCF-OcKa15oZdTefunwq0byWSP6lxq1EqxPjWG2W1NJK6YfTV4oaR30bfStsapmumvaplHaPpp_z6htNbOqqgRzPbvwgj06h3sGzNiuk0c-_P7cqa8lFd2vCrqs5FY9vA2f89-lZc0lN1bTb8igGvYtvF89_d7Lm3ZnCs13bv7j1h6U5h_UciVn1Jz6IYBe4IchCjwUIQii0IcERx6MIP…gAjyH4jDwcSe5NVwz8yr7fogAwsTHoDPUbpJZ-eUMIx875-uXqJk6MbnilXSjOGTaZoe23jXaDU8fgRiNBgT7QYIGJIgSMh7DmITeCIHBKAzhOCIeGjiuRbKMs9fl6nkyj7P1MunbcqJ-u4cf2f0E8Nt4Ws4W1-V7ukTxaBrEQJGAtNt33_5YbJ1Qb5kzqxdncJ4e1-dokmzhfg6eozRV3mK3GSzvq6kW4-EWeC5qZ9Vwg-c8mTi9B84xRw1ncTss2dA760leIUQyr3XgIb1cmpc8V5H7wdMWue4Nqs20SJGMVgTDolov4EvKGRGHdTMT_hnHp7d3dg8ug9n82rhWt0WLT4J71XV9_Mh_0CHyYhF4iWM659FReTMC3g5y-l4Q8Go4PGenQ-6fc7mojWpT23ysb_yGpudqdQWjOq844qhIi8kxjthHlg_hdXbO-KsURtwS_wbxBjaOfEs3ZNae8oNcLyv_SMok3O5PrtwECg3yME1wlGbb6_UpGLn1Ew",
    # "provider": "liveid"
}
c = {
    "provider": "liveid",
    "oauth": "refresh_token=MCU9u83i0GxVS19IP4vtLwtlbZuTGmxN9kjiXHP0J3D6bMeV711xzzRHfVs3PEwRU6jVLzTjg5dJ13DChOLw5f1VZiEh13sTshNZ*xaa5eeFgZVeBGX1GO1ndZwx3ddkgHRK821I1uGWvqZtxkd7c2leF2S5opd9BQ0Lw9rHC1n4dPIunpUmCaq6W9Py26XcJ92X6pXDL3mO4Pda2LxWhtESeCSpazTnT9W*mQHDKT1OkMkVMlPNrMBgE*lbnycSQjcJ!GS7nx4xgTwolZPoqTPcqlGlnFjLW89qXgv!B5332AXGzOqgxEEMFI7nlosLlX*LUFZBBeLBrBLIckasK4K1lBapy0!rmEMRbAGtkwK9u4xS!ToQAy9nRjdBT5N7Wo5wltcO9PYtwtVBMntovxrA%24",
    "redirect_uri": "https%3A%2F%2Foperatorportal.prodc.bce.tv3cloud.com%2Fworkflow%2Fproviderlist%2F",
    "access-token": "AuthToken1rVLLkto4FP2aZknpaewFC9uYhk7zNhjYdAlbBoFsGUlu6Hx9xFRnUpVkJptUqa50j859nCuFbSF4nfP-ydrGPOHwCQ3d0lx-iPrYMG0_uo1WBesect617ziXqi26uaocqzM2puX6p1hjzf-EPLg_qPmJV8x075U0ijVdpY8OvRlnEADUbf8YUfDaCvvhjrlkonrc16zifYgQZgVCZQFQ4OESYAx6BNLAK0pGadFZciarvhTvXBSdlNestuOiX_CStdJ2QinVjRffcfPvxdpw7Xh_TP9LAibl7xVWItfKqNJ-zuG7Rv-h0fsPjVpJ3j9wKd8qXghWCm3sWy7dg9k3c21Z8bdrqYZrZpXuhK09KS2-MitUPWHm0qfIR0HgUUQw8gJCgBdQH_qAQgQo8XrE9yEkgecBinqQ9hzddw7G-OEFOPB96gcEQuwR6HWSeyM0N7O6D6nnQr0AkE6sObO8-AR7GFAHzj57StWF1ytxrN2_jLm26amtDo0Wte0nBBPwKJ-EQ-i7cpDQaIiSmAxCigfER7HnD4ZJZzZPlmE6W67Gz9MwXS-T_kBrISjguycUlWhhdTTy0vY-Bre6CvamJtVl2zTblXQjisuz2RYLlmWN886JmgMJZ8yX9wYEfnjOzn5YmD2LkiBNrR0CeV1m1_G8dbmrLF1VAzust-ByidWJvSxO2TFKNjiAqkqqqAzLeZq7Z4zapleDrJxe0-Y1vX794qBgPipX-euhp0TiBbeo2kwdei53m2kCXS_HwYhQeDoWEUvkdP1qhhZ6zX7d1N7mPX6dvMglnwiaOZXDUN5heI_TzZ7t7J19jBz2POudeuhQEhyxMbluxi57NtOhaZ8327xe1GYngZ9MsgSMBpNzVuEvliJHWh9ykN6eZwosrmzvgHh3rEi6L8ciHvnjw8tiFV0Wg_KsTrtzJue3Jzxw6xs"
}


def mf_get_op_data(_uid, _env):
    env = str(_env)
    uid = str(_uid)
    cert = 'credentials/ossbssTools-proda-sts.pfx'
    cert_pass = 'Medi@F1rst'
    uid = str(_uid)
    # url = "https://appgw-client-a."+env+".bce.tv3cloud.com/s116/discovery/v3/programs/"+uid
    # url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/titles/'+uid
    url = 'https://operatorportal.' + env + '.bce.tv3cloud.com/apiproxy/UniversalService/v1/programs/' + uid
    # url = 'https://appgw-boss.'+env+'.bce.tv3cloud.com/oss/v1/universal-providers/tms/programs/' + uid
    # print("\r\nGet popularity")
    popularity = -1.00
    img_status = "Err"
    mf_matchstatus = "Err"
    # try:,
    try:
        # response = get(url, cookies=c, headers=pop_s.headers, verify=True, pkcs12_filename=cert, pkcs12_password=cert_pass)
        response = pop_s.get(url, cookies=c)  # , headers=token
        # print(response.text)
        rj = response.json()
        try:
            popularity = float(rj['Popularity'])
        except:
            popularity = -1.00
        try:
            mf_matchstatus = str(rj['MatchStatus'])
        except:
            mf_matchstatus = "Err"
        try:
            img_status = str(rj['ImagesState'])
        except:
            img_status = "Err"
    except:
        popularity = -1.00
        img_status = "Err"

    ret = {
        'op_popularity': popularity,
        "op_imagestatus": img_status,
        "op_matchstatus": mf_matchstatus
    }
    return ret


def connect_mongo(date_str, env):
    # try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    tablename = date_str + "_" + env
    mydb = myclient["ba-test"]
    mytab = mydb[tablename]
    mongo_connected = True
    # except:
    # mongo_connected = False
    # print("Alert: MongoDB is not connected!")
    return ({"Mongo_Connected": mongo_connected,
             "connection": mytab})


def mf_get_title(_uid, token, _env):
    uid = str(_uid)
    env = str(_env)
    # print('==> Getting title: ' + str(uid) +'\n')
    if env == "prodc":
        url = "https://appgw-client-a." + env + ".bce.tv3cloud.com/S116/discovery/v3/programs/" + uid
    else:
        url = "https://appgw-client-a." + env + ".bce.tv3cloud.com/S96/discovery/v3/programs/" + uid
    # print("URL: " + url)
    # try:
    # augmented_data = mf_get_op_data(uid)
    # popularity = augmented_data['popularity']
    # mf_imagestatus = augmented_data['mf_imagestatus']
    # try:
    # mf_matchstatus = augmented_data['mf_matchstatus']
    # except:
    # mf_matchstatus = "Err"
    # except:
    # popularity = -1
    # try:
    response = session.get(url)  # , headers=token
    try:
        rj = response.json()
        # print(rj)
        try:
            description = rj['Description']
        except:
            description = ""
        try:
            seriesid = rj['SeriesId']
        except:
            seriesid = "Error"
        try:
            title = rj['Name']
        except:
            title = "Error"
        try:
            inferred_oad = rj['OriginalAirDate']
        except:
            inferred_oad = "Error"
        try:
            inferred_language = rj['Locale']
        except:
            inferred_language = "Error"
        try:
            inferred_rating = rj['Ratings'][0]['Value']
        except:
            inferred_rating = "Error"
        try:
            episode_title = rj['EpisodeName']
        except:
            episode_title = ""
        try:
            images = rj['Images']
        except:
            images = []
        try:
            supported_images = rj['SupportedImages']
        except:
            supported_images = []

        res = {
            "inferred_k121": seriesid,
            "inferred_title": title,
            "inferred_episode_title": episode_title,
            "inferred_oad": inferred_oad,
            "inferred_language": inferred_language,
            "inferred_rating": inferred_rating,
            "inferred_description": description,
            "mf_images": images,
            "SupportedImages": supported_images
            # "mf_popularity": popularity,
            # "mf_imagestatus": mf_imagestatus,
            # "mf_matchstatus": mf_matchstatus
        }
    except:
        res = {
            "inferred_k121": "Error",
            "inferred_title": "Error",
            "inferred_episode_title": "Error",
            "inferred_oad": "Error",
            "inferred_language": "Error",
            "inferred_rating": "Error",
            "inferred_description": "Error",
            "mf_images": ["Error"],
            "SupportedImages": ["Error"]
            # "mf_popularity": "Error",
            # "mf_imagestatus": "Error",
            # "mf_matchstatus": "Error"
        }
    return res


def mf_map_program_parallel(seq_number, tok, date_str, env, past_ver):
    if past_ver == None:
        get_delta = False
    else:
        get_delta = True
    m = connect_mongo(date_str, env)
    mytab = m['connection']
    mongo_connected = m['Mongo_Connected']
    if (get_delta):
        m_past = connect_mongo(past_ver, env)  # added for glf delta logic
        m_past_connected = m_past['Mongo_Connected']
        pasttab = m['connection']  # added for past GLF delta logic
    if mongo_connected == False:
        return "Error - no mongo DB"
    while True:
        count_remaining = mytab.count_documents({"mf_uid": "*" + str(seq_number)})
        if (count_remaining == 0):
            break
        for doc in mytab.find({"mf_uid": "*" + str(seq_number)}).limit(50):
            pid = doc['pid']
            docid = doc['_id']
            ## Delta GLF logic
            glf_delta_string = "N/A"
            glf_new = False  # assume it is not new
            if get_delta == True:
                if pasttab.count_documents({"pid": pid}) == 0:
                    glf_delta_string = "glf_new"
                    glf_new = True
                else:
                    past_doc = pasttab.find({"pid": pid}).limit(1)[0]
                    columns = list(doc.keys())
                    glf_columns = [x for x in columns if 'glf_' in x]
                    glf_delta = False
                    # glf_error = False
                    # glf_delta_string = "glf"
                    for c in glf_columns:
                        # try:
                        # print("GLF Past: " + str(past_doc[c]) + "\r\n""GLF New: " + str(doc[c]))
                        if past_doc[c] != doc[c]:
                            # glf_delta_string += "_" + c
                            glf_delta = True
                    # except:
                    # pass #glf_delta_string = "error"
                    if glf_delta == False:
                        glf_delta_string = "glf_same"
                    else:
                        glf_delta_string = "glf_delta"
            else:
                pass
            ## End GLF delta logic
            uid = mf_map_program(pid, tok, env)
            title_data = mf_get_title(uid, tok, env)
            # guide image
            guide_image_status = mf_get_guide_poster(pid, env)
            # guide_image_status = "-1"
            ## Matching logic
            info = ""
            k119 = str(doc['glf_k119'])
            inferred_k119 = str(decode_tms(uid))
            if uid == "Error":
                info = "No ADP"
            elif (k119[0:3] != inferred_k119[0:3]) and (len(k119[0:3]) == len(inferred_k119[0:3])) and len(
                    k119[0:3]) == 3:
                info = k119[0:3] + "->" + inferred_k119[0:3]
            elif k119[0:2] in ("EP", "MV", "SH") and uid[0:4] == "fake":
                info = k119[0:3] + "->fake"
            elif (k119[0:2] in ("EP", "MV", "SH") and inferred_k119[0:2] in ("EP", "MV", "SH")) and (
                    k119[0:2] == inferred_k119[0:2]) and (k119 != inferred_k119):
                info = k119[0:2] + "->wrong " + inferred_k119[0:2]
            elif k119 == inferred_k119:
                info = "Matched-ok"
            elif k119 == "-1" and inferred_k119[0:2] in ("EP", "MV", "SH"):
                info = "No TMS -> " + inferred_k119[0:2]
            elif k119 == "-1" and "fake" in str(uid).lower():
                info = "Fake-ok"

            glf_k2 = str(doc['glf_k2'])
            k121_match = "Yes"
            k121 = str(doc['glf_k121'])
            inferred_k121 = str(decode_tms(title_data["inferred_k121"]))
            if (k121 == "-1"):
                k121_match = "NA-no k121"
            elif (len(inferred_k121) == 0):
                k_121_match = "NA-no inferred k121"
            elif (inferred_k121[0:6] == "series" and (glf_k2 in inferred_k121[6:-1])):
                k121_match = "Fake series but k2 match"
            elif (inferred_k121[0:6] == "series" and (glf_k2 not in inferred_k121[6:-1])):
                k121_match = "Fake series but no k2 match"
            elif inferred_k121 == "Error":
                k121_match = "NA-Error"
            elif (
                    k121 != inferred_k121):  # added logic to remove "_Series" from end of inferred_k121 in decode_tms method
                k121_match = "No"

            # Want to sese if inferred episode is not a part of inferred series
            subst_inf_k119 = inferred_k119[4:-4]
            subst_inf_k121 = inferred_k121[4:-4]
            # print(subst_inf_k119 + " " + subst_inf_k121)
            if inferred_k119 == "Error" or inferred_k121 == "Error":
                inferred_ep_in_series = "NA-Error"
            elif inferred_k119[0:2] != "EP" or inferred_k121[0:2] != "SH":
                if k121 == inferred_k121 and uid[0:4] == "fake":
                    inferred_ep_in_series = "Fake ep but yes"
                elif k121 != inferred_k121 and uid[0:4] == "fake":
                    inferred_ep_in_series = "Fake ep but no"
                else:
                    inferred_ep_in_series = "N/A-Not EP/SH"
            elif subst_inf_k119 == subst_inf_k121:
                inferred_ep_in_series = "Yes"
            else:
                inferred_ep_in_series = "No"
            title = doc['glf_title']
            inferred_title = title_data['inferred_title']
            if (inferred_title == "Error"):
                title_match = "NA-Error"
            elif (title != inferred_title):
                title_match = "No"
            else:
                title_match = "Yes"

            description = doc['glf_description']
            inferred_description = title_data["inferred_description"]
            if description == inferred_description:
                desc_match = "Yes"
            else:
                desc_match = "No"

            et = doc['glf_episode_title']
            inferred_et = title_data['inferred_episode_title']
            if et == inferred_et:
                et_match = "Yes"
            else:
                et_match = "No"

            # supported images
            image_guide_status = "No"
            image_adp_status = "No"
            image_hf_status = "No"
            image_4x3_status = "No"
            # try:
            if "SupportedImages" in title_data.keys():
                supported_images = title_data['SupportedImages']
                if len(list(supported_images)) > 0:
                    for size in supported_images:
                        # print("Size: " + size)
                        f = "NA"
                        if "poster" in size.lower():
                            f = "poster"
                        elif "keyart" in size.lower():
                            f = "keyart"
                        if "4x3" in size:
                            # 4x3 posters are used in recordings, guide
                            image_4x3_status = "Yes-" + f
                        elif "16x9" in size:
                            image_adp_status = "Yes-" + f
                        elif "2x3" in size:
                            image_hf_status = "Yes-" + f
                        elif "landscape" in size.lower():
                            # landscape is used in seasons adp
                            image_guide_status = "Yes-" + f
            # except:
            # pass
            ## Image Audit merged in here
            count_images = 0
            count_fails = 0
            tally_failed = 0
            res_images = dict()
            # count = 0
            try:
                for image in title_data['mf_images']:
                    size = image['Size']
                    url = image['Uri']
                    res_images[size] = url
            except:
                pass
            for size in res_images:
                count_images += 1
                # code = -1
                code = get_mf_image_status(res_images[size], str(k119+"-"+str(size)+".jpg"), env) # modified Jan 16, 2020 to add saving files to disk
                if int(code) != int(200):
                    count_fails += 1
                    tally_failed += 1
            if (count_images == 0):
                tally_failed += 1
            image_status_string = str(count_fails) + "/" + str(count_images) + " failed"

            # Get OP data for image
            if (match_op):
                # if k119[0:2] == "SH" and uid[0:4] != "fake":
                # op_uid = uid + "_Program"
                # else:
                op_uid = uid
                op_data = mf_get_op_data(op_uid, env)
                op_popularity = op_data['op_popularity']
                op_imagestatus = op_data['op_imagestatus']
                op_matchstatus = op_data['op_matchstatus']
            else:
                op_popularity = None
                op_imagestatus = None
                op_matchstatus = None

            update_data = {
                "mf_uid": str(uid),
                "mf_k119": inferred_k119,
                "mf_seriesid": str(title_data["inferred_k121"]),
                "mf_k121": inferred_k121,
                "mf_title": title_data["inferred_title"],
                "mf_episode_title": title_data["inferred_episode_title"],
                "mf_oad": title_data["inferred_oad"],
                "mf_language": title_data["inferred_language"],
                "mf_description": title_data["inferred_description"],
                "mf_rating": title_data["inferred_rating"],
                "mf_images": res_images,
                "mf_guide_image_status": guide_image_status,
                "match_k119": info,
                "match_k121": k121_match,
                "match_title": title_match,
                "match_episode_in_series": inferred_ep_in_series,
                "match_episode_title": et_match,
                "match_description": desc_match,
                "image_status": image_status_string,
                "image_guide_status": image_guide_status,
                "image_adp_status": image_adp_status,
                "image_hf_status": image_hf_status,
                "image_4x3_status": image_4x3_status,
                'op_popularity': op_popularity,
                "op_imagestatus": op_imagestatus,
                "op_matchstatus": op_matchstatus,
                "delta_glf": glf_delta_string
            }
            ## Delta MF logic
            delta_mf_string = "N/A"
            if get_delta == True:
                if glf_new == True:  # take short cut - no need to check if new again
                    delta_mf_string = "glf_new"
                else:
                    # past_doc = pasttab.find({"pid": pid}).limit(1)[0] # removed because this is already present from the GLF logic above
                    columns = list(past_doc.keys())  # short-cut: use columns from past
                    glf_columns = [x for x in columns if 'mf_' in x]
                    mf_delta = False
                    # glf_error = False
                    # glf_delta_string = "glf"
                    delta_cols = ["mf_delta"]
                    for c in glf_columns:
                        # try:
                        if past_doc[c] != update_data[
                            c]:  # short-cut: using update_data dictionary in lieu of querying for updated record from mongo
                            mf_delta = True
                            delta_cols.append(c)
                    # except:
                    # pass
                    if mf_delta == False:
                        delta_mf_string = "mf_same"
                    else:
                        delta_mf_string = ("-".join(delta_cols))
            else:
                pass
            ## End MF delta logic
            update_data['delta_mf'] = delta_mf_string

            ret = mytab.update_one({"_id": docid}, {"$set": update_data})
    return

def isInCatalogue(string):
    tok = get_token('OSS', 'proda', list())
    hex = string.encode('utf-8').hex()

    uid = "746D73ThirdParty" + hex
    session = requests.Session()
    session.headers = tok

    env = str('proda')

    url = "https://appgw-client-a." + env + ".bce.tv3cloud.com/S96/discovery/v3/programs/" + uid

    response = session.get(url)  # , headers=token

    if str(response.status_code) == '200':
        try:
            rj = response.json()
        except:
            return False
            try:
                description = rj['Description']
            except:
                description = ""
            try:
                seriesid = rj['SeriesId']
            except:
                seriesid = "Error"
            try:
                title = rj['Name']
            except:
                title = "Error"
            try:
                inferred_oad = rj['OriginalAirDate']
            except:
                inferred_oad = "Error"
            try:
                inferred_language = rj['Locale']
            except:
                inferred_language = "Error"
            try:
                inferred_rating = rj['Ratings'][0]['Value']
            except:
                inferred_rating = "Error"
            try:
                episode_title = rj['EpisodeName']
            except:
                episode_title = ""
            try:
                images = rj['Images']
            except:
                images = []
            try:
                supported_images = rj['SupportedImages']
            except:
                supported_images = []
            try:
                showName = rj['Name']
            except:
                showName = "test"
            return True #It does exists
    else:
        return False

def getProgramList_Schedules(programID_main,schedules):

    scheduledList = []
    for schedule in schedules:
        #This is to loop through each of the scheduled recordings
        programID_schedule = schedule.attrib['p']
        if programID_schedule == programID_main:
            try:
                row = {}
                timeFrame = schedule.attrib['d']
                schedule_frame = schedule.attrib['s']
                channelLeter = schedule.attrib['c']
                row['Time Frame'] = timeFrame
                row['Schedule Time'] = schedule_frame
                row['Channel Letter'] = channelLeter
                scheduledList.append(row)

            except:
                timeFrame = ""
    return scheduledList #Return the list which means we have properly populated it

if __name__ == '__main__':
    allList = []
    #seq_max = mp.cpu_count()
    # seq_max = 1
    env = "proda"
    print("Using environment: " + str(env))

    tok = get_token('OSS',env, list())
    tok["User-Agent"] = "Microsoft-IPTV-Client/1.6 (Linux; Mediaroom 1.1.2402.5090; MPF 1.1; MPF 3.0; MediaFirst; DVR; ARRIS; VIP5662W; HEVC)"
    tok["MPF-AccessControl"] = "P:1,1 A:1,1 R:0,0 RT:1,0 UTL:0,0 AAP:0 BMGD:1 BMS:0 BUR:0"

    out_file_name = "_output.txt"
    allPrograms = 0
    problematic = 0
    #epg_file = "C://Users//Me//Downloads//EPGFILES//EPGFILES//EPG_v3263-5842445530034343718.xml"
    mypath = "C://Users//Me//Downloads//EPGFILES//EPGFILES//"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    epgNumber = 0
    epg_file = "C://Users//Me//Desktop//EPG_v3413-7502016412994468142.xml"

    #for eachFile in onlyfiles:
        #print("Analyzing " + eachFile)
        #currEPG = []
    with open(epg_file, 'r', encoding="UTF-8") as xmlfile:
        seq_count = 0  # set as 0->4 for a total of 5 threads

        tree = ET.parse(xmlfile)
        root = tree.getroot()[0]
        programs = root.find("programs")
        schedules = root.find("schedules")

        ## Start with parsing programs - get all programs.
        # Look for unique episodes (k.119 != k1.121) vs generic episodes (k.119 == k.121)
        #programs = root.find("programs")

        # stop_count = 30
        for program in programs:  # try for just 1 program)
            allPrograms += 1
            # stop_count -= 1
            # if (stop_count == 0):
            # break
            # print("Program starting")
            k119 = -1  # episode
            k121 = -1  # series
            k2 = -1  # root ID from GN
            k100 = ""  # rating

            try:
                d = program.attrib['d'].replace("|", "/").replace('\n', '')  # get program description from GLF
            except:
                d = ""
            try:
                title = program.attrib['t'].replace("|", "/").replace('\n', '')  # get program title from GLF
            except:
                title = ""
            try:
                episode_title = program.attrib['et'].replace("|", "/").replace('\n', '')
            except:
                episode_title = ""
            try:
                lang = str(program.attrib['l'])
            except:
                lang = ""
            try:
                programID_main = program.attrib['id']
            except:
                programID_main = None
            id = 0

            #now that we have a program ID, we will use that to find the list of series assets that do not exist in the catagolog
            # ----------------------------#
            programs_scheduleList = []
            programID_scheduleList = getProgramList_Schedules(programID_main,schedules)
            count = -1
            for eachEPG in onlyfiles:
                count += 1
                eacg = mypath + eachEPG

                with open(eacg, 'r', encoding="UTF-8") as eachXML:

                    tree1 = ET.parse(eachXML)
                    root1 = tree1.getroot()[0]
                    programs_eachXML = root1.find("programs")
                    schedules_eachXMl = root1.find("schedules")

                    flag = False

                    for program_eachXML in programs_eachXML:  # try for just 1 program)

                        try:
                            programID_eachXML = program.attrib['id']
                        except:
                            programID_eachXML = None

                        if programID_main == programID_eachXML and programID_eachXML != None:

                            programID_scheduleList_eachXML = getProgramList_Schedules(programID_eachXML, schedules_eachXMl)

                            #if programID_scheduleList_eachXML != programID_scheduleList:
                            #Then we want to check each proram
                            for eachTimeFrame in programID_scheduleList:
                                timeFrame = eachTimeFrame['Time Frame']
                                scheduleTime = eachTimeFrame['Schedule Time']
                                channelLetter = eachTimeFrame['Channel Letter']

                                for eachTimeFrame_XML in programID_scheduleList_eachXML:
                                    timeFrame_XML = eachTimeFrame_XML['Time Frame']
                                    scheduleTime_XML = eachTimeFrame_XML['Schedule Time']
                                    channelLetter_XML = eachTimeFrame_XML['Channel Letter']

                                    #print(channelLetter_XML)

                                    if channelLetter == channelLetter_XML and scheduleTime == scheduleTime_XML:
                                        #print(timeFrame_XML + " to " + timeFrame)
                                        if timeFrame != timeFrame_XML:
                                            print("Then the show has extended from " + timeFrame + " to " + timeFrame_XML)
                                            problematic += 1

                                #print("Then we have a discrepancy with " + programID_main  + " ON EPG # " + str(count))
                                #print(programID_scheduleList_eachXML)
                                #print(programID_scheduleList)

                                flag = True
                        if flag == True:
                            break
        print(problematic/allPrograms)

