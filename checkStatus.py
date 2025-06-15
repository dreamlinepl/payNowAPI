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
from datetime import datetime
from config import service_id, key, BASE_URL

def calculate_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def check_transaction(orderID):
    # Wygeneruj hash zapytania
    data_to_hash = [service_id, orderID, key]
    string_to_hash = '|'.join(data_to_hash)
    hash_value_req = calculate_sha256(string_to_hash)

    print(f"\n[{datetime.now().isoformat()}] Checking Order ID: {orderID}")

    payload = urllib.parse.urlencode({
        "ServiceID": service_id,
        "OrderID": orderID,
        "Hash": hash_value_req
    })

    headers = {
        'BmHeader': 'pay-bm',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    url = BASE_URL + '/webapi/transactionStatus'
    response = requests.request("POST", url, headers=headers, data=payload)

    root = ET.fromstring(response.text)
    transaction = root.find('.//transaction')
    if transaction is not None:
        orderID = transaction.find('orderID').text
        remoteID = transaction.find('remoteID').text
        amount = transaction.find('amount').text
        currency = transaction.find('currency').text
        paymentStatus = transaction.find('paymentStatus').text
        hash_value_answ = root.find('hash').text
        service_id_response = root.find('serviceID').text

        # UWAGA: Poprawna kolejność z serviceID
        data = [
            service_id_response,
            orderID,
            remoteID,
            amount,
            currency,
            paymentStatus,
            key
        ]
        response_hash_string = '|'.join(data)
        calculated_hash = calculate_sha256(response_hash_string)

        print("Remote ID:", remoteID)
        print("Amount:", amount)
        print("Currency:", currency)
        print("Status:", paymentStatus)

        if calculated_hash == hash_value_answ:
            print("✅ Hash OK")
        else:
            print("❌ Hash mismatch")
    else:
        print("❌ No <transaction> found in response")

# Lista zamówień do sprawdzenia
orderIDs = ["3100528", "3768754"]

for order_id in orderIDs:
    check_transaction(order_id)
