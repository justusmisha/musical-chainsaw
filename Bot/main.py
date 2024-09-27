import os
# import aio_pika
from aiogram import executor

from Bot.app.handlers import dp
#
# RABBITMQ_USER = str(os.getenv("RABBITMQ_USER"))
# RABBITMQ_PASS = str(os.getenv("RABBITMQ_PASS"))
# RABBITMQ_HOST = str(os.getenv("RABBITMQ_HOST"))
# RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}/"


if __name__ == "__main__":
    executor.start_polling(dp)
