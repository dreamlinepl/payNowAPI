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
from datetime import datetime
from config import service_id, key, BASE_URL


def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hashxxxxx``
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

order_id = str(random.randint(1000000, 9999999))
amount = "3500.00"
gateway_id = "1500"
currency = "EUR"
user_email= 'mlody@email.com'
language ="EN"
Hold = "true"

data = [service_id, 
        order_id, 
        amount, 
        gateway_id, 
        currency, 
        user_email, 
        language,
        Hold, 
        key]

string_to_hash='|'.join(data)
print (string_to_hash)
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
    "Hold" : Hold,
    "Hash" : hash_value_req
    }

print("\n[{}] Request:".format(datetime.now().isoformat()))
print (data)
payload = urllib.parse.urlencode(data)

headers = {
  'BmHeader': 'pay-bm-continue-transaction-url',
  'Content-Type': 'application/x-www-form-urlencoded',
}

url = BASE_URL+'/payment'
response = requests.request("POST", url, headers=headers, data=payload)
print("\n[{}] RESPONSE /payment:".format(datetime.now().isoformat()))
print(response.text)
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

print("Remote ID:", remoteID)
print("Order ID:", orderID)
print("Status:", status)
print("Redirect URL:", redirecturl)

if hash_value == hash_value_answ:
    print("✅ Hash OK")
else:
    print("❌ Hash mismatch")