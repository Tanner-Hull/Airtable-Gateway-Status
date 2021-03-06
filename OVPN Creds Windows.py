# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:17:21 2020

@author: Tanner Hull
"""

import requests
from datetime import datetime
import os
import time
from airtable import Airtable


numList = ['0','1','2','3','4','5','6','7','8','9']
API_KEYSF = 'API_KEY'
API_KEYEG = 'API_KEY'
API_KEYS_ENGAGE = {"damarend":'API_KEY',"bears.gendunas":'API_KEY',
                   "indarset":'API_KEY',"selareon":'API_KEY'}

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


table = Airtable('appdOXoC877tSErXd', "GatewayStatus", api_key = 'API_KEY')

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
                      "Last Update": str(datetime.now()),
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
                      "Last Update": str(datetime.now()),
                      "Country Number": country}
                table.update(j["id"], fields)
                
for key in API_KEYS_ENGAGE:
    os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command silent_connection"')
    if key == "damarend":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command connect Damarend.ovpn"')
        time.sleep(15)
    elif key == "bears.gendunas":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command connect Gendunas.ovpn"')
        time.sleep(15)
    elif key == "indarset":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command connect Indarset.ovpn"')
        time.sleep(15)
    elif key == "selareon":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command connect Selareon.ovpn"')
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
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command disconnect Damarend.ovpn"')
    elif key == "bears.gendunas":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command disconnect Gendunas.ovpn"')
    elif key == "indarset":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command disconnect Indarset.ovpn"')
    elif key == "selareon":
        os.system('cmd /c ""C:/Program Files/OpenVPN/bin/openvpn-gui.exe" --command disconnect Selareon.ovpn"')

