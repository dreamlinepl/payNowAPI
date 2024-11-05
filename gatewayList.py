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
import json

def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

service_id = "1001811"

MessageID = str(uuid.uuid4().hex)
currencies = "EUR, PLN"


key = '6baf1f3abb21cff7060be697a8769d8c25055c63aaf4d3afb995272be8e158b8'
key = '52dc6665dcb40484389f5a2bd233d3c160b4e2e4'

data = [service_id, MessageID, currencies, key]

string_to_hash='|'.join(data)
print (string_to_hash)
# print (string_to_hash)
hash_value_req=calculate_sha256(string_to_hash)
print (hash_value_req)

data = {
    "ServiceID": service_id ,
    "MessageID": MessageID,
    "Currencies" : currencies,
    "Hash" : hash_value_req
    }
# print (data)

payload = json.dumps(data)

headers = {
  'BmHeader': 'pay-bm',
  'Content-Type': 'application/json',
}

url = "https://pay.autopay.eu/gatewayList/v2"
# url = "https://testpay.autopay.eu/gatewayList/v2"
response = requests.request("POST", url, headers=headers, data=payload)
print (response.text)
# Parse the XML data
root = ET.fromstring(response.text)