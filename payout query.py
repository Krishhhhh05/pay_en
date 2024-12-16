import requests
import hashlib

# Define constants
PAYOUT_QUERY_URL = "https://sandbox.wpay.one/v1/Query/Payout"
API_KEY = "eb6080dbc8dc429ab86a1cd1c337975d"  # Replace with your actual API key

# Function to generate the signature
def generate_signature(params, api_key):
    sorted_params = sorted(params.items())
    param_string = "&".join(f"{key}={value}" for key, value in sorted_params if value)
    param_string += f"&key={api_key}"
    return hashlib.md5(param_string.encode('utf-8')).hexdigest().lower()

def query_payout(mch_id, out_trade_no):
    """
    Query the payout API with the given mchId and out_trade_no.
    """
    # Prepare request parameters
    params = {
        "mchId": mch_id,
        "out_trade_no": out_trade_no,
    }

    # Generate the signature
    params["sign"] = generate_signature(params, API_KEY)

    try:
        # Make the API request
        response = requests.post(PAYOUT_QUERY_URL, data=params)

        # Handle the response
        if response.status_code == 200:
            response_data = response.json()
            print("API Response:", response_data)
            return response_data
        else:
            print("Error:", response.status_code, response.text)
            return {"error": response.text, "status_code": response.status_code}

    except Exception as e:
        print("Exception occurred:", str(e))
        return {"error": str(e)}

# Input query parameters
mch_id = "1000"
out_trade_no = "20241217022728"

# Call the function
response = query_payout(mch_id, out_trade_no)
print("Final Output:", response)
