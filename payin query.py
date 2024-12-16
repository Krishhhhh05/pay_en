import hashlib
import requests

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

# API details and parameters
api_url = "https://sandbox.wpay.one/v1/Query/Collect"
api_key = "eb6080dbc8dc429ab86a1cd1c337975d"

# Request parameters for Query Collect API
params = {
    "mchId": "1000",
    "out_trade_no": "2024121612000002"  # The unique transaction/order ID
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
        # Extract and display transaction status
        status = response_data["data"].get("status")
        print(f"Transaction Status: {status}")
    else:
        print("API Error:", response_data.get("msg"))
else:
    print("HTTP Error:", response.status_code)
    print("Response Content:", response.text)
