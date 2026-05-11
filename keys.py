import os
from dotenv import load_dotenv

load_dotenv()  # загружает .env

###### КОНСТАНТЫ ИЗ .ENV ######
SR_LOGIN = os.getenv('sr_login')  # Ваш демо-ключ
SR_PASS = os.getenv('sr_pass')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')
DB_SCHEMA = os.getenv('db_schema')
DB_DATABASE = os.getenv('db_database')

LOG = os.getenv('login')
PASS = os.getenv('password')

BOT_TOKEN=os.getenv('bot_token')
BOT_NAME=os.getenv('bot_name')

###### ТЕКСТЫ ######
HELP_TEXT = """
/add_client Имя Телефон
...
"""
