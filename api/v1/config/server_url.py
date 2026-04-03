import os
from dotenv import load_dotenv
load_dotenv()
SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
if not SERVER_HOST:
    raise ValueError("SERVER_HOST environment variable is not set")
if not SERVER_PORT:
    raise ValueError("SERVER_PORT environment variable is not set")
