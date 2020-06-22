#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:17:21 2020

@author: Tanner Hull
"""

import requests
import datetime
import os
import time
from airtable import Airtable
from pytz import timezone
import subprocess


numList = ['0','1','2','3','4','5','6','7','8','9']
API_KEYSF = '217669dae8b94ec4a36e1372eb800346'
API_KEYEG = 'c6e07870463c56c66e798cd2b598aef2a17bcc3a'
API_KEYS_ENGAGE = {"damarend":'b3ed9aff9d694c070d4e15c794eba627a16dfdb6',"bears.gendunas":'2ab3efe7a2ebc64fe36f43589686e76ad84f2afe',
                   "indarset":'722deed594eaf12317661840d4a0007d2a64b42f',"revercut":'4edaeac4d791eefc8ace8b79489b1f6fb4eb990e ',
                   "selareon":'e8a25f460c413947c9ba6c8cd9f890d9152828ba'}

headers = {
  'Authorization': 'Token ' + API_KEYSF
}
head = {
  'Authorization': 'Token ' + API_KEYEG
        }

response1 = requests.get("https://www.scalefusion.com/api/v1/devices.json?page=1", headers = headers)
response2 = requests.get("https://www.scalefusion.com/api/v1/devices.json?page=2", headers = headers)
engageResponse = requests.get("https://engage.istpulse.com/api/v2/channels.json", headers = head)

jsonData1 = response1.json()
jsonData2 = response2.json()
EGjson = engageResponse.json()


table = Airtable('appdOXoC877tSErXd', "GatewayStatus", api_key = 'key78f4mMjdb7AEBc')

devicesList = table.get_all()


for i in jsonData1["devices"]:
    if i["device"]["group"]["name"] == 'Global Ops - No PIA' or i["device"]["group"]["name"] == 'Global OPS':
        if i["device"]["locked"] == True:
            t = "LOCKED"
        else:
            t = "UNLOCKED"
            
        if i["device"]["name"][0] in numList:
            country = i["device"]["name"][:3]
        elif i["device"]["name"][0] == "Y":
            country = i["device"]["name"][0]
        else:
            country = "X"
        for j in devicesList:
            if j["fields"]["Gateway Name"] == i["device"]["name"]:
                fields = {"Gateway Name": i["device"]["name"], 
                      "Scalefusion Last Check-In": i["device"]["last_connected_at"][:10] + " " + i["device"]["last_connected_at"][11:-5],
                      "Engage Last Check-In": 'N/A',
                      "Network Type": 'N/A',
                      "Locked/Unlocked": t,
                      "Last Update": str(datetime.datetime.now(tz=timezone("EST"))),
                      "Country Number": country}
                table.update(j["id"], fields)
                
for i in jsonData2["devices"]:
    if i["device"]["group"]["name"] == 'Global Ops - No PIA' or i["device"]["group"]["name"] == 'Global OPS':
        if i["device"]["locked"] == True:
            t = "LOCKED"
        else:
            t = "UNLOCKED"
            
        if i["device"]["name"][0] in numList:
            country = i["device"]["name"][:3]
        elif i["device"]["name"][0] == "Y":
            country = i["device"]["name"][0]
        else:
            country = "X"
        for j in devicesList:
            if j["fields"]["Gateway Name"] == i["device"]["name"]:
                fields = {"Gateway Name": i["device"]["name"], 
                      "Scalefusion Last Check-In": i["device"]["last_connected_at"][:10] + " " + i["device"]["last_connected_at"][11:-5],
                      "Engage Last Check-In": 'N/A',
                      "Network Type": 'N/A',
                      "Locked/Unlocked": t,
                      "Last Update": str(datetime.datetime.now(tz=timezone("EST"))),
                      "Country Number": country}
                table.update(j["id"], fields)
                
for key in API_KEYS_ENGAGE:
    #os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command silent_connection"')
    if key == "damarend":
        d = subprocess.Popen(["openvpn", "--config", "/opt/vpn_profiles/damarend/config.conf"])
        time.sleep(15)
    elif key == "bears.gendunas":
        b = subprocess.Popen(["openvpn", "--config", "/opt/vpn_profiles/bears/config.conf"])
        time.sleep(15)    
    elif key == "indarset":
        ind = subprocess.Popen(["openvpn", "--config", "/opt/vpn_profiles/indarset/config.conf"])
        time.sleep(15)
    elif key == "selareon":
        s = subprocess.Popen(["openvpn", "--config", "/opt/vpn_profiles/selareon/config.conf"])
        time.sleep(15)
    elif key == "revercut":
        r = subprocess.Popen(["openvpn", "--config", "/opt/vpn_profiles/revercut/config.conf"])
        time.sleep(15)
        
    
    
    head = {
    'Authorization': 'Token ' + API_KEYS_ENGAGE[key]
          }
    
    engageResponse = requests.get("https://engage." + key + ".com/api/v2/channels.json", headers = head)
    EGjson = engageResponse.json()
    
    
    
    
    for i in EGjson["results"]:
        for j in devicesList:
            if i["name"] == j["fields"]["Gateway Name"]:
                fields = {
                    "Engage Last Check-In": i["last_seen"][:10] + " " + i["last_seen"][11:-8],
                    "Network Type": i["device"]["network_type"]
                    }
                table.update(j["id"], fields)

    
    if key == "damarend":
        d.terminate()
    elif key == "bears.gendunas":
        b.terminate()    
    elif key == "indarset":
        ind.terminate()
    elif key == "selareon":
        s.terminate()
    elif key == "revercut":
        r.terminate()
