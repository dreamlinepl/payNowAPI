# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 21:28:47 2023

@author: Marcin
"""

import requests
import json
import hmac
import hashlib
import base64
import webbrowser
import uuid
import time
import sys

def calculate_hmac(data, key):
    hashed_object = hmac.new(key, data, hashlib.sha256).digest()
    return base64.b64encode(hashed_object)

def processing_spinner(duration):
    # Define the spinner characters (you can customize these)
    spinner = ['*', '**', '***', '****','*****', '******', '*******', '********']

    # Calculate the number of iterations based on the duration
    iterations = int(duration / len(spinner))

    for _ in range(iterations):
        for frame in spinner:
            sys.stdout.write(f"\rProcessing {frame}")
            sys.stdout.flush()
            time.sleep(0.5)  # Adjust the sleep time as needed

    # Clear the line after the spinner
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()



user_email = input("Enter user email:")
# user_email = "test@test.pl"
user_travel_id = input('Enter travel Id:')
# user_travel_id ="#T3G4"
currency = ""
user_amount = input("Enter amount:")
user_amount = float(user_amount) * 100
user_amount = int(user_amount)

while True:
    currency = input('Which currency, PLN or EUR: ').strip().lower()

    if currency == 'eur':
        currency = "EUR" 
        break
    elif currency == 'pln':
        currency = "PLN"
        break
    else:
        print("**** Please enter 'EUR' or 'PLN'.****")


payload = json.dumps({
  "amount": user_amount,
  "externalId": "99b09681-2fa8-4e0d-bf87-2aeeca2807b6",
  "description": "Zamówienie samolotu: " + user_travel_id,
  "currency": currency,
  "paymentMethodId": 2002,
   "buyer": {
    "email": user_email
   }
})

# wawrtosci z mBanku:
api_key = '693f5aa4-4ebb-4673-96e6-9735f4fdedb7'
signature_key = '14260cfa-9c78-4f38-850f-de5224c95d97'

# unikalny identifier losowy
idempotency_key = str(uuid.uuid4())

# hashowanie podpisu wiadomosci
signature = calculate_hmac(payload.encode(), signature_key.encode())

headers = {
  'Api-Key': api_key,
  'Signature': signature,
  'Idempotency-Key': idempotency_key,
  'Content-Type': 'application/json'
}
url = "https://api.sandbox.paynow.pl/v1/payments"

response = requests.request("POST", url, headers=headers, data=payload)
python_dict = json.loads(response.text)
redirectURL = python_dict["redirectUrl"]
paymentId = python_dict ["paymentId"]
ststus = python_dict ["status"]

webbrowser.open(redirectURL)
print ("The payment link created successfully!")
print (redirectURL)

processing_spinner(5)

#%%

url = "https://api.sandbox.paynow.pl/v1/payments/" + paymentId + "/status"
payload = {}
headers = {
  'Api-Key': api_key
}

while  True:
    processing_spinner(8)
    response = requests.request("GET", url, headers=headers, data=payload) 
    python_dict = json.loads(response.text)
    status = python_dict ["status"]
    if status == "CONFIRMED" :
        print("Payment is completed successfully.")
        break  # Exit the loop

    
    
    
    