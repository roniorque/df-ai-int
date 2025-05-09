import os
import json
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def collect_telemetry(data):
    """
    Sends JSON data to a remote MongoDB instance.

    Args:
        data (dict): The JSON data to send.
    """
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("Telemetry skipped, no database configured.")
        return

    try:
        
        # Get the current UTC time
        utc_now = datetime.now(timezone.utc)

        # Define the GMT+8 timezone offset
        gmt_plus_8 = timezone(timedelta(hours=8))

        # Convert the UTC time to GMT+8
        timestamp = utc_now.astimezone(gmt_plus_8).isoformat()
        data['timestamp'] = timestamp
        
        client = MongoClient(mongodb_uri)
        db = client.get_database()  # Use the default database specified in the URI
        collection = db["df_data"]  # Replace "telemetry" with your desired collection name
        collection.insert_one(data)
        print("Data successfully sent to MongoDB.")
    except Exception as e:
        print(f"Error sending data to MongoDB: {e}")
    finally:
        client.close()

def clear_collection(data):
    """
    Deletes all documents from a specified MongoDB collection.
    """
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("Deletion skipped: No database configured.")
        return

    try:
        client = MongoClient(mongodb_uri)
        db = client.get_default_database()
        collection = db[f"{data}"]  # Replace with your collection name
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents from the collection.")
    except Exception as e:
        print(f"Error deleting documents: {e}")
    finally:
        client.close()
