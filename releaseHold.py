# releaseHold.py
"""
Created on Thu Sep  7 21:28:47 2023

@author: Marcin
"""

import requests
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
import uuid
from config import service_id, key, BASE_URL

def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash


remoteID = "A91M334UUP"
message_id = uuid.uuid4().hex



data = [service_id,
        message_id,
        remoteID,
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
    "Hash" : hash_value_req
    }

payload = urllib.parse.urlencode(data)

headers = {
  'BmHeader': 'pay-bm',
  'Content-Type': 'application/x-www-form-urlencoded',
}

url = BASE_URL+'/webapi/transactionCancel'
response = requests.request("POST", url, headers=headers, data=payload)
#print (response.text)
# Parse the XML data
root = ET.fromstring(response.text)

# Access elements within the XML
service = root.find('serviceID').text
messageID = root.find('messageID').text
confirmation = root.find('confirmation').text
reason = root.find('reason').text
hash_value_answ = root.find('hash').text

#Mandatory response hash check
data = [service, messageID, confirmation, reason, key]
string_to_hash ='|'.join(data)
hash_value=calculate_sha256(string_to_hash)

print("Reason:", reason)\

if hash_value == hash_value_answ:
    print("✅ Hash OK")
else:
    print("❌ Hash mismatch")





