import hashlib
import requests
from pymongo import MongoClient
from datetime import datetime
import uuid

# Function to generate the signature
def generate_signature(params, api_key):
    sorted_params = sorted(params.items())
    param_string = "&".join(f"{key}={value}" for key, value in sorted_params if value)
    param_string += f"&key={api_key}"
    return hashlib.md5(param_string.encode('utf-8')).hexdigest().lower()

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["wpay_transactions"]
collection = db["payins"]

# API details and parameters
api_url = "https://sandbox.wpay.one/v1/Collect"
api_key = "eb6080dbc8dc429ab86a1cd1c337975d"

# Generate a unique order ID
unique_order_id = 2024121613000002  # Generates a unique hexadecimal string

# Request parameters
params = {
    "mchId": "1000",
    "currency": "BDT",
    "out_trade_no": unique_order_id,  # Use the unique order ID
    "pay_type": "BKASH",
    "money": "100",
    "attach": "",
    "notify_url": "https://www.sandbox.wpay.one/callback/payin",
    "returnUrl": "https://www.google.com"
}

# Generate the signature
params["sign"] = generate_signature(params, api_key)
print("order_no",unique_order_id )

# Make the API request
response = requests.post(api_url, data=params)

# Print and process the response
if response.status_code == 200:
    response_data = response.json()
    print("API Response:", response_data)
    
    if response_data.get("code") == 0:
        data = {
            "merchant_id": params["mchId"],
            "order_details": {
                "order_id": params["out_trade_no"],
                "transaction_id": response_data["data"].get("transaction_Id"),
                "currency": params["currency"],
                "payment_type": params["pay_type"],
                "amount": int(params["money"]),
                "status": response_data.get("msg"),
                "payment_url": response_data["data"].get("url")
            },
            "callback_url": params["notify_url"],
            "timestamp": datetime.utcnow().isoformat()
        }

        # Insert into MongoDB
        # inserted_id = collection.insert_one(data).inserted_id
        # print(f"PayIn data inserted into MongoDB with ID: {inserted_id}")
        # print("payin data",data)
    else:
        print("API Error:", response_data.get("msg"))
else:
    print("HTTP Error:", response.status_code)
    print("Response Content:", response.text)