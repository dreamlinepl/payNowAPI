# checkStatus.py
"""
Created on Thu Sep  7 21:28:47 2023
@author: Marcin
"""

import requests
import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
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
    #print(response.text)

    transactions = root.findall('.//transaction')
    hash_value_answ = root.find('hash').text
    service_id_response = root.find('serviceID').text

    if not transactions:
        print("❌ No <transaction> found in response")
        return

    # Budowanie stringa do hasha
    response_string_parts = [service_id_response]

    for t in transactions:
        response_string_parts.append(t.find('orderID').text)
        response_string_parts.append(t.find('remoteID').text)
        response_string_parts.append(t.find('amount').text)
        response_string_parts.append(t.find('currency').text)

        gateway = t.find('gatewayID')
        if gateway is not None and gateway.text:
            response_string_parts.append(gateway.text)

        payment_date = t.find('paymentDate')
        if payment_date is not None and payment_date.text:
            response_string_parts.append(payment_date.text)

        response_string_parts.append(t.find('paymentStatus').text)

        details = t.find('paymentStatusDetails')
        if details is not None and details.text:
            response_string_parts.append(details.text)

    response_string_parts.append(key)
    full_response_string = '|'.join(response_string_parts)

    #print("📦 Full response string to hash:")
    #print(full_response_string)

    calculated_hash = calculate_sha256(full_response_string)

    #print("✅ Hash calculated:", calculated_hash)
    #print("🔐 Hash from response:", hash_value_answ)

    if calculated_hash == hash_value_answ:
        print("✅✅ All transaction hash OK")
    else:
        print("❌❌ Hash mismatch for multiple transactions")

    # Opcjonalnie wypisz każdą transakcję
    for t in transactions:
        print("\n➡️ Transaction details:")
        print("  Order ID:      ", t.find('orderID').text)
        print("  Remote ID:     ", t.find('remoteID').text)
        print("  Amount:        ", t.find('amount').text)
        print("  Currency:      ", t.find('currency').text)
        print("  Status:        ", t.find('paymentStatus').text)
        payment_date_raw = t.find('paymentDate')
        if payment_date_raw is not None and payment_date_raw.text:
            try:
                dt = datetime.strptime(payment_date_raw.text, "%Y%m%d%H%M%S")
                formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = f"⚠️ Invalid format: {payment_date_raw.text}"
        else:
            formatted_date = "N/A"

        print("  Payment Date:  ", formatted_date)
        print("  Details:       ", t.find('paymentStatusDetails').text if t.find('paymentStatusDetails') is not None else 'N/A')


# Lista zamówień do sprawdzenia
orderIDs = [
    "39236597-7636194",
    "39236597-7630643",
    "39236597-7624172",
    "39236597-7617791",
    "39256156-2273064",
    "39256156-2266253",
    "39256156-2262472",
    "39256156-2255191",
]

for order_id in orderIDs:
    check_transaction(order_id)
