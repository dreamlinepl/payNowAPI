# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 21:28:47 2023

@author: Marcin
"""

import requests
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
from config import service_id, key, BASE_URL

def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

amount = "1532.00"
remoteID = "ABE7U1BJLN"
message_id = uuid.uuid4().hex




data = [service_id,
        message_id,
        remoteID,
        amount,
        key]

string_to_hash='|'.join(data)
print (string_to_hash)
# print (string_to_hash)
hash_value_req=calculate_sha256(string_to_hash)
# print (hash_value)

data = {
    "ServiceID": service_id ,
    "MessageID": message_id,
    "RemoteID": remoteID,
    "Amount": amount,
    "Hash" : hash_value_req
    }

print("\n[{}] Request:".format(datetime.now().isoformat()))
print (data)
payload = urllib.parse.urlencode(data)

headers = {
  'BmHeader': 'pay-bm',
  'Content-Type': 'application/x-www-form-urlencoded',
}

url = BASE_URL+'/webapi/transactionClear'
response = requests.request("POST", url, headers=headers, data=payload)
print (response.text)
# Parse the XML data
root = ET.fromstring(response.text)