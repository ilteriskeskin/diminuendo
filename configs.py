import os

from dotenv import load_dotenv

load_dotenv()

URI = os.environ.get('DB_URI')
NAME = os.environ.get('DB_NAME')
SECRET_KEY = os.environ.get('SECRET_KEY')
