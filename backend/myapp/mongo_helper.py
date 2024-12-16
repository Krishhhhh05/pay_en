from pymongo import MongoClient
from django.conf import settings
from django.http import JsonResponse

class MongoDBHelper:
    def __init__(self):
        # Ensure that settings.MONGO_URI is a valid string
        if not isinstance(settings.MONGO_URI, str):
            raise ValueError("Invalid MONGO_URI in settings")

        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client['payment']  # Database name
        self.collection = self.db['payin']  # Collection name
        

def get_latest_document_value(self):
        latest_doc = self.collection.find_one(sort=[('_id', -1)])  # Get the latest document by _id
        if latest_doc:
            print(latest_doc)
            # return latest_doc.get('value', None)
        return None

# def insert_to_payin(self, data, doc_id):
# try:
#             payin_collection = self.db['payin']  # Define collection explicitly
#             result = payin_collection.insert_one({"data": data, "id": doc_id})
#             return {"success": True, "inserted_id": str(result.inserted_id)}
#         except errors.PyMongoError as e:
#             return {"success": False, "error": str(e)}


