# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 21:28:47 2023

@author: Marcin
"""

import requests
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
import random


def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

service_id = "1001811"
order_id = str(random.randint(1000000, 9999999))
amount = "29.00"
gateway_id = "1503"
currency = "EUR"
user_email= 'marcin.szpecht@volanti.vip'
language ="EN"
RecurringAcceptanceState = "NOT_APPLICABLE"
RecurringAction = 'AUTO'
ClientHash = '572d8e3ae70aec3035753c5dfa223fbf73d4a53a'

key = '52dc6665dcb40484389f5a2bd233d3c160b4e2e4'

data = [service_id, 
        order_id, 
        amount, 
        gateway_id, 
        currency, 
        user_email, 
        language, 
        RecurringAcceptanceState, 
        RecurringAction, 
        ClientHash,
        key]

string_to_hash='|'.join(data)
print (string_to_hash)
# print (string_to_hash)
hash_value_req=calculate_sha256(string_to_hash)
# print (hash_value)

data = {
    "ServiceID": service_id ,
    "OrderID": order_id ,
    "Amount": amount,
    "GatewayID" : gateway_id,
    "Currency" : currency,
    "CustomerEmail" : user_email,
    "Language" : language,
    "RecurringAcceptanceState" : RecurringAcceptanceState,
    "RecurringAction" : RecurringAction,
    "ClientHash": ClientHash,
    "Hash" : hash_value_req
    }

payload = urllib.parse.urlencode(data)

headers = {
  'BmHeader': 'pay-bm-continue-transaction-url',
  'Content-Type': 'application/x-www-form-urlencoded',
}

url = "https://testpay.autopay.eu/payment"
response = requests.request("POST", url, headers=headers, data=payload)
print (response.text)
# Parse the XML data
root = ET.fromstring(response.text)

# Access elements within the XML
status = root.find('status').text
redirecturl = root.find('redirecturl').text
orderID = root.find('orderID').text
remoteID = root.find('remoteID').text
hash_value_answ = root.find('hash').text

#Mandatory response hash check
data = [status, redirecturl, orderID, remoteID, key]
string_to_hash ='|'.join(data)
hash_value=calculate_sha256(string_to_hash)

if hash_value == hash_value_answ:
        print("Status:", status)
        print("Redirect URL:", redirecturl)