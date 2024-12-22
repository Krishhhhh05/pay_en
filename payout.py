import hashlib
import requests
from pymongo import MongoClient
from datetime import datetime
import uuid

# Function to generate the signature
def generate_signature(params, api_key):
    # Step 1: Sort parameters lexicographically by key
    sorted_params = sorted(params.items())
    
    # Step 2: Concatenate key-value pairs into a query string
    param_string = "&".join(f"{key}={value}" for key, value in sorted_params if value)
    
    # Step 3: Append the API key
    param_string += f"&key={api_key}"
    
    # Step 4: Generate MD5 hash and return the lowercase result
    return hashlib.md5(param_string.encode('utf-8')).hexdigest().lower()

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["wpay_transactions"]
collection = db["payouts"]  # Store Payout transactions in a separate collection

# API details and parameters
api_url = "https://sandbox.wpay.one/v1/Payout"
api_key = "eb6080dbc8dc429ab86a1cd1c337975d"

# Generate a unique order ID
unique_order_id = str(uuid.uuid4().hex)  # Generates a unique hexadecimal string

# Request parameters for the Payout API
params = {
    "mchId": "1000",
    "currency": "BDT",
    "out_trade_no": unique_order_id,  # Use the unique order ID
    "pay_type": "BKASH",
    "account": "03123456789",
    "userName": "zhang san",  # Space in name will be URL-encoded automatically by `requests`
    "money": "100",
    "attach": "",
    "notify_url": "https://www.sandbox.wpay.one/callback/payout",
    "reserve1": "1234567890123"
}

# Generate the signature
params["sign"] = generate_signature(params, api_key)

# Make the API request
response = requests.post(api_url, data=params)

# Print and process the response
if response.status_code == 200:
    response_data = response.json()
    print("API Response:", response_data)
    
    if response_data.get("code") == 0:
        # Extract relevant data for MongoDB
        data = {
            "merchant_id": params["mchId"],
            "order_details": {
                "order_id": params["out_trade_no"],
                "transaction_id": response_data["data"].get("transaction_Id"),
                "currency": params["currency"],
                "payment_type": params["pay_type"],
                "account": params["account"],
                "username": params["userName"],
                "amount": int(params["money"]),
                "status": response_data.get("msg"),
                "callback_url": params["notify_url"]
            },
            "timestamp": datetime.utcnow().isoformat()
        }

        # Insert into MongoDB
        inserted_id = collection.insert_one(data).inserted_id
        print(f"Payout data inserted into MongoDB with ID: {inserted_id}")
    else:
        print("API Error:", response_data.get("msg"))
else:
    print("HTTP Error:", response.status_code)
    print("Response Content:", response.text)
