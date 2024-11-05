import hashlib

service_id = "161412"
order_id = "7033-29-ec1f3009-d445fd10"
remote_id = "AXUIB318WT"
amount = "89.90"
currency = "PLN"
gateway_id = "1503"
payment_date = "20241105073211"
payment_status = "SUCCESS"
payment_status_details = "AUTHORIZED"
customerEmail ="test3@gmail.com"
recurringAction= "INIT_WITH_PAYMENT"
clientHash= "b25828fabb128ec57d3187c1dccf6b7666ab6b9b"
expirationDate= "20270430235959"
cardData_index = "20513244"
validityYear="2027"
validityMonth="04"
issuer="VISA"

# Ensure key is correct and in the expected format
key = 'e85f67ff92cae6b311eab770e9de6a5ad702a8db67f6f9138ddb1bd81796661c'


# Prepare data for hashing, ensuring all parts match expected format
data_list = [
    service_id,
    order_id,
    amount,
    currency,
    gateway_id,
    payment_date,
    payment_status,
    payment_status_details,
    customerEmail,
    recurringAction,
    clientHash,
    expirationDate,
    cardData_index,
    validityYear,
    validityMonth,
    issuer,
    key
]

# Join the data into a single string with '|' separator
string_to_hash = '|'.join(data_list)

# Calculate SHA-256 hash
def calculate_sha256(data): 
    if isinstance(data, str):
        data = data.encode()
    sha256_hash = hashlib.sha256(data).hexdigest()
    return sha256_hash

hash_value = calculate_sha256(string_to_hash)

# Output results
print("String to hash:", string_to_hash)
print("SHA-256 Hash:", hash_value)
