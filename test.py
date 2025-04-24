from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Get MongoDB URI from environment variable
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    print("Error: MONGO_URI environment variable is not set. Please check your .env file.")
    exit(1)

try:
    client = MongoClient(mongo_uri)
    print("Successfully connected to MongoDB!")
    print("Server info:", client.server_info())
except Exception as e:
    print("Error connecting to MongoDB:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nPlease check:")
    print("1. Your .env file exists and contains MONGO_URI")
    print("2. Your MongoDB server is running")
    print("3. The connection string is correct")
    print("4. Your network allows the connection")
