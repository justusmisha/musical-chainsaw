import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URLS = os.getenv('BASE_URLS')
SCHOOL_INFO = 'Наша школа ...'
ERROR_MESSAGE = '❌ Возникла проблема'
CLASSES_INFO = "Краткая информация о всех классах"
SCHOOL_CONTACT_NUMBER = "+7(999)999-99-99"
SCHOOL_FOOD_INFO = "Информация о питании\n\nТрех-разовое разовое питание"
SCHOOL_FOOD_PRICE = 3000
SCHOOL_URL = 'https://krylia-nn.ru'
SCHOOL_3D_URL = SCHOOL_URL + '/3d-ekskursiya-po-shkole.html'
SCHOOL_DOCS_URL = SCHOOL_URL + '/prajs/napravleniya/dokumentyi-2.html'