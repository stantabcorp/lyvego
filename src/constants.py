import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
PORT = 3306
DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
API_KEY = os.getenv("API_KEY")
AUTHORIZATION = os.getenv("AUTHORIZATION")
TOKEN = os.getenv("TOKEN")
TOKEN_DEBUG = os.getenv("TOKEN_DEBUG")
API_ROOT = os.getenv("API_ROOT")
SENTRY_TOKEN = os.getenv("SENTRY_TOKEN")
TOPGG_API_KEY = os.getenv("TOPGG_API_KEY")