import logging

# Create a custom app_logger
logger = logging.getLogger(__name__)

# Set the minimum level of logger_data for the app_logger
logger.setLevel(logging.INFO)  # Capture all log levels, including DEBUG

# Create handlers
file_handler = logging.FileHandler('app.log')
console_handler = logging.StreamHandler()

# Set the level for each handler
file_handler.setLevel(logging.DEBUG)  # Capture all log levels, including DEBUG
console_handler.setLevel(logging.DEBUG)  # Capture all log levels, including DEBUG

# Create formatters and add them to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the app_logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
