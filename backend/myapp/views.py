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
from urllib.parse import urlencode
from urllib.parse import parse_qs


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
address= "https://api.wpay.one"
PAYIN_API= "https://sandbox.wpay.one/v1/Collect"
PAYIN_API2= "https://api.wpay.one/v1/Collect"
PAYOUT_API= "https://sandbox.wpay.one/v1/Payout"
PAYOUT_API2= "https://api.wpay.one/v1/Payout"
BALANCE_API = "https://api.wpay.one/v1/balance"
# https://{{host}}/v1/balance
PAYIN_QUERY_URL= "https://sandbox.wpay.one/v1/Query/Collect"
PAYOUT_QUERY_URL= "https://sandbox.wpay.one/v1/Query/Payout"
API_KEY = "eb6080dbc8dc429ab86a1cd1c337975d"
API_KEY2="af566094b5a5412cb28a2b7d7b09d06a"
PAYIN_CALLBACK= "https://www.sandbox.wpay.one/callback/payin"



@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # Find the user in MongoDB
            mongo_helper = MongoDBHelper()
            users_collection = mongo_helper.db['users']
            
            user = users_collection.find_one({"username": username})
            if not user:
                return JsonResponse({"error": "Invalid username or password"}, status=401)

            # Verify the password
            if password != user["password"]:
                return JsonResponse({"error": "Invalid username or password"}, status=401)

            # Authentication successful
            return JsonResponse({"success": "Login successful", "role": user["role"]}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)



@csrf_exempt
def create_admin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            percent= data.get("percent")
            role = "admin"  # Fixed role for admins
            balance = 0

            # Check if required fields are provided
            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # Initialize MongoDBHelper and connect to 'users' collection
            mongo_helper = MongoDBHelper()
            users_collection = mongo_helper.db["users"]

            # Check if the username already exists
            if users_collection.find_one({"username": username}):
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Insert the new admin user into the collection
            user_data = {
                "username": username,
                "password": password,
                "percent": percent,
                "role": role,
                "balance": balance
            }
            users_collection.insert_one(user_data)

            return JsonResponse({"success": "Admin created successfully", "username": username}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_admin(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            username = data.get("username")

            if not username:
                return JsonResponse({"error": "Username is required"}, status=400)

            mongo_helper = MongoDBHelper()
            users_collection = mongo_helper.db["users"]

            if users_collection.find_one({"username": username}):
                users_collection.delete_one({"username": username})

            return JsonResponse({"success": "Admin removed successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_users(request):
    if request.method == "GET":
        try:
            mongo_helper = MongoDBHelper()
            users_collection = mongo_helper.db["users"]
            users = list(users_collection.find({}, {"_id": 0, "username": 1, "percent": 2 ,"role": 3}))
            return JsonResponse({"users": users}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use GET."}, status=405)

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
            params["sign"] = generate_signature(params, API_KEY2)

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
def get_admins_balance(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))
            username = body.get("username")


            mongo_helper = MongoDBHelper()
            collection = mongo_helper.db["test"]
            
            txn = list(collection.find({"username": username}, {"_id": 0}))

            return JsonResponse({"users": txn}, status=200)
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
    if request.method == "POST":
        try:
            # Parse form-encoded data
            if request.POST:
                body_input = request.body.decode('utf-8')
                body = parse_qs(body_input)

                print(body)

                mch_id = body.get('mchId', [None])[0]
                username= body.get('userName', [None])[0]
                currency = body.get('currency', [None])[0]
                pay_type = body.get('pay_type', [None])[0]
                money = float(body.get('money', [None])[0])
                notify_url = body.get('notify_url', [None])[0]
                return_url = body.get('returnUrl', [None])[0]
                percent= float(body.get('percent', [None])[0])

                # Print extracted fields
                print("Merchant ID:", mch_id)
                print("Username:", username)
                print("percent:", percent)
                print("Currency:", currency)
                print("Payment Type:", pay_type)
                print("Money:", money)
                print("Notify URL:", notify_url)
                print("Return URL:", return_url)

            if not all([mch_id, username,currency, pay_type, money, notify_url, return_url]):
                return JsonResponse({"error": "Missing required parameters."}, status=400)
            
            # Generate a unique order ID
            payin_order_id = generate_transaction_id()

            # Prepare request parameters for external API
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
            params["sign"] = generate_signature(params, API_KEY2)
            print("params",params)
            encoded_data = urlencode(params)
            print("encoded_data",encoded_data)
            # Send request to external API (form-encoded)
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "charset": "UTF-8"  # Ensure UTF-8 encoding is specified
            }

            # Send POST request
            response = requests.post(
                PAYIN_API2,
                data=encoded_data, 
                headers=headers
            )
            print("response",response.text)
            
            # Calculate real_money
            real_money = money - (money * (percent / 100))
            real_money = f"{real_money:.2f}" 
            print("real money",real_money)
            
            data = {
                "username": username,
                "money": money,
                "out_trade_no": payin_order_id,
                "real_money": real_money,
                "percent": percent,
                "currency": currency,
                "pay_type": pay_type,
                
            }
            

            # Handle external API response
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("code") == 0:
                    print("in response")
                    mongo_helper = MongoDBHelper()
                    user_db = mongo_helper.db[username]  # Select or create the database named after the username

                    # # Insert the document into the 'payout' collection
                    result = user_db.insert_one(data)

                    # Convert ObjectId to a string
                    inserted_id = str(result.inserted_id)
                    print("inserted_id",inserted_id)
                    return JsonResponse({
                        "success": True,
                        "data": response_data.get("data", {})
                    }, status=201)
                else:
                    return JsonResponse({"error": response_data.get("data")}, status=400)
            else:
                return JsonResponse({
                    "error": "External API request failed.",
                    "details": response.text
                }, status=response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Use POST."}, status=405)

@csrf_exempt
def payout_api(request):
    if request.method == "POST":
        try:
            # Parse request body
            if request.POST:
                body_input = request.body.decode('utf-8')  
                print("body_input",body_input)
                body = parse_qs(body_input)
                

                    
                mch_id = body.get('mchId', [None])[0]# Default to None if key not found
                currency = body.get('currency', [None])[0]
                pay_type = body.get('pay_type', [None])[0]
                account = body.get('account', [None])[0]
                money = body.get('money', [None])[0]
                username = body.get('userName', [None])[0]

                # Print extracted fields
                print("Merchant ID:", mch_id)
                print("Currency:", currency)
                print("Payment Type:", pay_type)
                print("Account:", account)
                print("Money:", money)
                print("Username:", username)

                
                


                if not all([mch_id, currency, pay_type, account, money,username]):
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
                    "notify_url": "callback_payout_url",
                    # "reserve1": reserve1
                }
                

                # Generate the signature
                params["sign"] = generate_signature(params, API_KEY2)

                # Make the API request
                response = requests.post(PAYOUT_API2, data=params)

                if response.status_code == 200:
                    response_data = response.json()
                    print("response_data",response_data)

                    if response_data.get("code") == 0:

                        transaction_id = response_data["data"].get("transaction_Id")

                        # Prepare data for MongoDB
                        data = {
                            "merchant_id": mch_id,
                          
                                "order_id": payin_order_id,
                                "transaction_id": transaction_id,
                                "currency": currency,
                                "payment_type": pay_type,
                                "account": account,
                                "username": username,
                                "amount": int(money),
                                "status": response_data.get("msg"),
                                "callback_url": "callback_payout_url",
                            
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        # print("data",data)  
                        
                        # Insert into MongoDB
                        # inserted_id = collection.insert_one(data).inserted_id
                        mongo_helper = MongoDBHelper()
                        payout_collection = mongo_helper.db['payout']  # Explicitly specify the collection

                        # Insert the document into the 'payin' collection
                        result = payout_collection.insert_one(data)

                        # Convert ObjectId to a string
                        inserted_id = str(result.inserted_id)
                        print("inserted_id",inserted_id)

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
        print("Raw request body:", request.body)
        body = json.loads(request.body.decode("utf-8"))
        print("body load done",body)
        mongo_helper = MongoDBHelper()
        payin_collection = mongo_helper.db['payin']

        result= payin_collection.insert_one(body)
        inserted_id = str(result.inserted_id)
        print("inserted_id",inserted_id)
        print("payin",)
        return JsonResponse({"success": "success"}, status=200)
    
       
    except Exception as e:
        # Catch-all for unexpected errors
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)
