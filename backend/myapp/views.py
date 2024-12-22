from datetime import datetime
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import requests
import json
from .mongo_helper import MongoDBHelper
from pymongo import MongoClient
import urllib.parse
import pymongo
import time


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




import random

def generate_transaction_id():
    # Get the current date and time
    now = datetime.now()  # Correct usage of utcnow()

    # Format the date and time as YYYYMMDDHHMMSS
    timestamp = now.strftime("%Y%m%d%H%M%S")
    if int(timestamp[-1]) % 2 != 0:
        # If the last digit is odd, add 1 to make it even
        timestamp = timestamp[:-1] + str((int(timestamp[-1]) + 1) % 10)


    # Concatenate the timestamp and random sequence to form the transaction ID
    transaction_id = timestamp
    return transaction_id


# API details
PAYIN_API= "https://sandbox.wpay.one/v1/Collect"
PAYOUT_API= "https://sandbox.wpay.one/v1/Payout"
BALANCE_API = "https://sandbox.wpay.one/v1/balance"
PAYIN_QUERY_URL= "https://sandbox.wpay.one/v1/Query/Collect"
PAYOUT_QUERY_URL= "https://sandbox.wpay.one/v1/Query/Payout"
API_KEY = "eb6080dbc8dc429ab86a1cd1c337975d"
API_KEY2="af566094b5a5412cb28a2b7d7b09d06a"
PAYIN_CALLBACK= "https://www.sandbox.wpay.one/callback/payin"
@csrf_exempt
def get_balance(request):
    if request.method == "POST":
        try:
            # Parse request body
            body = json.loads(request.body.decode('utf-8'))

            # Required parameters
            mch_id = body.get("mchId")
            currency = body.get("currency")

            if not mch_id or not currency:
                return JsonResponse({"error": "Missing required parameters: mchId and currency."}, status=400)

            # Request parameters
            params = {
                "mchId": mch_id,
                "currency": currency
            }

            # Generate the signature
            params["sign"] = generate_signature(params, API_KEY)

            # Make the API request
            response = requests.post(BALANCE_API, data=params)

            # Handle the external API response
            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0:
                    # Extract balance information
                    balance = response_data["data"].get("balance")
                    return JsonResponse({"balance": balance, "currency": currency}, status=200)
                else:
                    return JsonResponse({"error": response_data.get("msg")}, status=400)
            else:
                return JsonResponse({"error": "External API request failed.", "details": response.text}, status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)

@csrf_exempt
def payin_query(request):
    if request.method == "POST":
        try:
            # Parse request body
            body = json.loads(request.body.decode('utf-8'))

            # Required parameters
            mch_id = body.get("mchId")
            out_trade_no = body.get("out_trade_no")

            if not mch_id or not out_trade_no:
                return JsonResponse({"error": "Missing required parameters: mchId and out_trade_no."}, status=400)

            # Request parameters
            params = {
                "mchId": mch_id,
                "out_trade_no": out_trade_no
            }

            # Generate the signature
            params["sign"] = generate_signature(params, API_KEY)
            print("params",params)
            # Make the API request
            response = requests.post(PAYIN_QUERY_URL, data=params)

            # Handle the external API response
            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0:
                    # Extract transaction status
                    status = response_data["data"].get("status")
                    
                    return JsonResponse({"response": response_data}, status=200)
                else:
                    return JsonResponse({"error": response_data.get("msg")}, status=400)
            else:
                return JsonResponse({"error": "External API request failed.", "details": response.text}, status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)


@csrf_exempt
def payout_query(request):
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body)

            mch_id = body.get("mchId")
            out_trade_no = body.get("out_trade_no")

            if not mch_id :
                return JsonResponse({"error": "Missing required parameters. id"}, status=400)
            if not out_trade_no:
                            return JsonResponse({"error": "Missing required parameters. trade no"}, status=400)

            # Prepare request parameters
            params = {
                "mchId": mch_id,
                "out_trade_no": out_trade_no,
            }

            # Generate the signature
            params["sign"] = generate_signature(params, API_KEY)

            # Make the API request
            response = requests.post(PAYOUT_QUERY_URL, data=params)

            if response.status_code == 200:
                response_data = response.json()
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({"error": "External API request failed.", "details": response.text}, status=response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)

payin_order_id=""
@csrf_exempt
def payin_api(request):
    global payin_order_id
    if request.method == "POST":
        try:
            # Parse request body
            body = json.loads(request.body.decode('utf-8'))

            # Required parameters
            mch_id = body.get("mchId")
            currency = body.get("currency")
            pay_type = body.get("pay_type")
            money = body.get("money")
            notify_url = body.get("notify_url")
            return_url = body.get("returnUrl")

            if not all([mch_id, currency, pay_type, money, notify_url, return_url]):
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            # Generate a unique order ID
            payin_order_id = generate_transaction_id()
            # payin_order_id = 20211012151100001

            # Request parameters
            params = {
                "mchId": mch_id,
                "currency": currency,
                "out_trade_no": payin_order_id,
                "pay_type": pay_type,
                "money": money,
                "attach": body.get("attach", ""),
                "notify_url": notify_url,
                "returnUrl": return_url
            }
 

            # Generate the signature
            params["sign"] = generate_signature(params, API_KEY)

            # Make the API request
            response = requests.post(PAYIN_API, data=params)

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0:

                    print("in code 0")

                    # transaction_id = response_data["data"].get("transaction_Id")
                    payment_url = response_data["data"].get("url")
                    
                    timestamp = generate_transaction_id()
                   
                    mongo_helper = MongoDBHelper()
                    payin_collection = mongo_helper.db['payin']  # Explicitly specify the collection

                    # Insert the document into the 'payin' collection
                    result = payin_collection.insert_one(response_data)
                    # payin_callback(request,response_data)
                    return JsonResponse({
                        "success": True, 
                        "data": dict(response_data.get("data", {}).items()),  # Convert dict_items to a regular dict
                       
                    }, status=201)  
                else:
                    return JsonResponse({"error": response_data.get("msg")}, status=400)
            else:
                return JsonResponse({"error": "External API request failed.", "details": response.text}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)

@csrf_exempt
def payout_api(request):
    if request.method == "POST":
        try:
            # Parse request body
            body = json.loads(request.body.decode('utf-8'))

            # Required parameters
            mch_id = body.get("mchId")
            currency = body.get("currency")
            pay_type = body.get("pay_type")
            account = body.get("account")
            username = body.get("userName")
            money = body.get("money")
            notify_url = body.get("notify_url")
            reserve1 = body.get("reserve1")

            if not all([mch_id, currency, pay_type, account, username, money, notify_url]):
                return JsonResponse({"error": "Missing required parameters."}, status=400)

            # Generate a unique order ID
            # payin_order_id = str(uuid.uuid4().hex)
            payin_order_id = generate_transaction_id()

            # Request parameters
            params = {
                "mchId": mch_id,
                "currency": currency,
                "out_trade_no": payin_order_id,
                "pay_type": pay_type,
                "account": account,
                "userName": username,
                "money": money,
                "attach": body.get("attach", ""),
                "notify_url": notify_url,
                "reserve1": reserve1
            }

            # Generate the signature
            params["sign"] = generate_signature(params, API_KEY)

            # Make the API request
            response = requests.post(PAYOUT_API, data=params)

            if response.status_code == 200:
                response_data = response.json()

                if response_data.get("code") == 0:
                    transaction_id = response_data["data"].get("transaction_Id")

                    # Prepare data for MongoDB
                    data = {
                        "merchant_id": mch_id,
                        "order_details": {
                            "order_id": payin_order_id,
                            "transaction_id": transaction_id,
                            "currency": currency,
                            "payment_type": pay_type,
                            "account": account,
                            "username": username,
                            "amount": int(money),
                            "status": response_data.get("msg"),
                            "callback_url": notify_url
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    print("data",data)  

                    # Insert into MongoDB
                    # inserted_id = collection.insert_one(data).inserted_id
                    mongo_helper = MongoDBHelper()
                    payout_collection = mongo_helper.db['payout']  # Explicitly specify the collection

                    # Insert the document into the 'payin' collection
                    result = payout_collection.insert_one(data)

                    # Convert ObjectId to a string
                    # inserted_id = str(result.inserted_id)

                    # Return a JSON response
                    return JsonResponse({
                        "success": True, 
                        "data": dict(response_data.get("data", {}).items()),
                       
                    }, status=201)
                else:
                    return JsonResponse({"error": response_data.get("msg")}, status=400)
            else:
                return JsonResponse({"error": "External API request failed.", "details": response.text}, status=response.status_code)

        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)

@csrf_exempt
def payin_callback(request):
    global payin_order_id
    print("In payin callback",payin_order_id)

    try:
       
        try:
            body = json.loads(request.body.decode("utf-8"))
            print("body load done",body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body."}, status=400)

        # Extract required fields from the body
        try:
            mch_id = body.get("mchId")
            currency = body.get("currency")
            money = body.get("money")

            if not all([mch_id, currency, money]):
                return JsonResponse({"error": "Missing required parameters."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key in request body: {str(e)}"}, status=400)

        try:
            # Convert and calculate money values
            money = float(money)
            merchant_ratio = float(body.get("merchant_ratio", 5))  # Default to 5% if not provided
            real_money = money - (money * merchant_ratio / 100)
        except ValueError:
            return JsonResponse({"error": "Invalid value for money or merchant_ratio."}, status=400)

        # Construct data for callback
        try:
            data = {
                "mch_id": mch_id,
                "out_trade_no": payin_order_id,  # Ensure this is set globally
                "currency": currency,
                "money": money,
                "attach": "",
                "pay_money": money,
                "merchant_ratio": 5,
                "real_money": f"{real_money:.2f}",
                "status": 1,
            }
            data["sign"] = generate_signature(data, API_KEY)
            print("data",data)
        except Exception as e:
            return JsonResponse({"error": f"Error constructing callback data: {str(e)}"}, status=500)
        print("done with data",data)
        # Send the callback request
        try:
            response = requests.post(PAYIN_CALLBACK, data=data)
            response.raise_for_status()  # Raise HTTP errors if any
            return JsonResponse(response.json(), status=200)
        except requests.RequestException as e:
            return JsonResponse({
                "error": "Failed to send callback request.",
                "details": str(e),
            }, status=500)

    except Exception as e:
        # Catch-all for unexpected errors
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
