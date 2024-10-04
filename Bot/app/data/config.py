import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URLS = os.getenv('BASE_URLS')
SCHOOL_INFO = 'Наша школа ...'
ERROR_MESSAGE = 'Возникла проблема'