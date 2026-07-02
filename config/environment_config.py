from dotenv import load_dotenv
import os
import const
load_dotenv()

LOG_FILE_PATH = "D:\\DataEngineer\\trace-insight\\ErrorAnalyzerAgent\\resources\\enterprise-payment-service.log"
LOG_START_PATTERN = const.LOG_START_PATTERN
DATE_FIELD=const.DATE_FIELD
TIME_FIELD=const.TIME_FIELD
LOG_LEVEL=const.LOG_LEVEL
LOG_MESSAGE=const.LOG_MESSAGE
MONGODB_URI=const.MONGODB_URI
MONGODB_DB=const.MONGODB_DB
MONGODB_COLLECTION=const.MONGODB_COLLECTION


def get_required_env() -> dict:
    """
    Returns the value of the required environment variable.
    Raises an exception if it is not set.
    """
    value = os.getenv(LOG_START_PATTERN)
    if not value:
        raise ValueError(
            f"Required environment variable '{LOG_START_PATTERN}' is not set in the .env file."
        )
    date_field = os.getenv(DATE_FIELD)
    if not date_field:
        raise ValueError(f"Required environment variable '{DATE_FIELD}' is not set in the .env file.")

    time_field = os.getenv(TIME_FIELD)
    if not time_field:
        raise ValueError(f"Required environment variable '{TIME_FIELD}' is not set in the .env file.")

    log_level_field = os.getenv(LOG_LEVEL)
    if not log_level_field:
        raise ValueError(f"Required environment variable '{LOG_LEVEL}' is not set in the .env file.")

    log_message_field = os.getenv(LOG_MESSAGE)
    if not log_message_field:
        raise ValueError(f"Required environment variable '{LOG_MESSAGE}' is not set in the .env file.")

    mongodb_uri = os.getenv(MONGODB_URI)
    if not mongodb_uri:
        raise valueError(f"required environment variable '{MONGODB_URI}' is not set in the .env file.")

    mongodb_db = os.getenv(MONGODB_DB)
    if not mongodb_db:
        raise ValueError(f"required environment variable '{MONGODB_DB}' is not set in the .env file.")

    mongodb_collection = os.getenv(MONGODB_COLLECTION)
    if not mongodb_collection:
        raise valueError(f"required environment variable '{MONGODB_COLLECTION}' is not set in the .env file")

    return {LOG_START_PATTERN: value, DATE_FIELD: int(date_field), TIME_FIELD: int(time_field),
            LOG_LEVEL: int(log_level_field), LOG_MESSAGE: int(log_message_field),
            MONGODB_URI: mongodb_uri,MONGODB_DB: mongodb_db,MONGODB_COLLECTION: mongodb_collection}