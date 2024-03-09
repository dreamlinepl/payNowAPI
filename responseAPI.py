# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:15:06 2023

@author: Marcin
"""
import requests
import xml.etree.ElementTree as ET
import base64
import hashlib
from datetime import datetime

def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    # Calculate SHA-256 hash
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

service_id = "1000351"
order_id = "25328818-2445792"
amount = "4000.00"
currency = "EUR"
gateway_id = "0"
key = '3dcda8051d4028f01190e841c42708e5a57981c7'
remote_id = "AHZ6TSJ37Z"
paymentDate = datetime.now().strftime("%Y%m%d%H%M%S") # Set payment date to current date and time,
paymentStatus = "SUCCESS"
paymentStatusDetails="AUTHORIZED"



# service_id = "1"
# order_id = "11"
# remote_id = "91"
# amount = "11.11"
# gateway_id = "1"
# currency = "PLN"
# key = '1test1'
# paymentDate = "20010101111111"
# paymentStatus = "SUCCESS"
# paymentStatusDetails="AUTHORIZED"


# Create the XML data with the transactions element Base64-encoded
root = ET.Element("transactionList")
serviceID = ET.SubElement(root, "serviceID")
serviceID.text = service_id
transactions = ET.SubElement(root, "transactions")
transaction_data = {
    "orderID": order_id,
    "remoteID": remote_id,
    "amount": amount,
    "currency": currency, #Note that the currency and gatewayID is swapped in the ITN
    "gatewayID": gateway_id,
    "paymentDate": paymentDate, 
    "paymentStatus": paymentStatus,
    "paymentStatusDetails": paymentStatusDetails
}


transaction_element = ET.Element("transaction")
for tag, value in transaction_data.items():
    sub_element = ET.SubElement(transaction_element, tag)
    sub_element.text = value    
base64_encoded_data = base64.b64encode(ET.tostring(transaction_element)).decode("utf-8")
transactions.text = base64_encoded_data

data = [service_id, order_id, remote_id, amount, gateway_id, currency, paymentDate, paymentStatus, paymentStatusDetails, key]
string_to_hash='|'.join(data)
# print (string_to_hash)
hash_value=calculate_sha256(string_to_hash)
# print (hash_value)

hash_element = ET.SubElement(root, "hash")
hash_element.text = hash_value


# Serialize the ElementTree to a string
xml_string = ET.tostring(root, encoding="utf-8").decode("utf-8")
# print (xml_string)

url = 'https://payment.amcaviation.eu/status'

headers = {
    'Content-Type': 'application/xml',
}

# Send the POST request with the XML data
# response = requests.post(url, data=xml_string, headers=headers)
response = requests.request("POST", url, headers=headers, data=xml_string)
print(response.text)
print(response.status_code)


# if response.status_code == 200:
#     print("Request was successful.")
#     print(response.text)
# else:
#     print("Request failed with status code:", response.status_code)
