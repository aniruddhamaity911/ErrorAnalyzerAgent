"""
logIngestion.py
This file contain methods that's extract ERROR logs from
passed log file and store it in vector store
"""

import os
from dotenv import load_dotenv
import re
from Error import ErrorLog
load_dotenv()

LOG_FILE_PATH = "D:\\DataEngineer\\trace-insight\\ErrorAnalyzerAgent\\resources\\enterprise-payment-service.log"
LOG_START_PATTERN = "LOG_START_PATTERN"
DATE_FIELD="DATE_FIELD"
TIME_FIELD="TIME_FIELD"
LOG_LEVEL="LOG_LEVEL"
LOG_MESSAGE="LOG_MESSAGE"


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

    return {"LOG_START_PATTERN": value, "DATE_FIELD": int(date_field), "TIME_FIELD": int(time_field),
            "LOG_LEVEL": int(log_level_field), "LOG_MESSAGE": int(log_message_field)}


def extract_error_logs(log_file_path: str):
    """
    Extracts complete ERROR log blocks, including stack traces.
    """
    environment_vars = get_required_env()
    pattern = environment_vars.get(LOG_START_PATTERN)
    date_field = environment_vars.get(DATE_FIELD)
    time_field = environment_vars.get(TIME_FIELD)
    log_level_field = environment_vars.get(LOG_LEVEL)
    log_message_field = environment_vars.get(LOG_MESSAGE)
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    if not isinstance(date_field, int):
        raise TypeError("date_field must be an int")

    if not isinstance(time_field, int):
        raise TypeError("time_field must be an int")

    if not isinstance(log_level_field, int):
        raise TypeError("log_level_field must be an int")

    if not isinstance(log_message_field, int):
        raise TypeError("log_message_field must be an int")

    log_start_pattern = re.compile(pattern)
    capturing = False
    current_error = []
    error_level = "ERROR"
    current_timestamp = ""
    current_level = ""
    current_message = ""
    error_logs = []
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            # New log entry
            if log_start_pattern.match(line):
                # Save previous error block
                if capturing:
                    error_logs.append(
                        ErrorLog(
                            timestamp=current_timestamp,
                            level=current_level,
                            message=current_message,
                            raw_error="".join(current_error)
                        )
                    )
                    capturing = False
                    current_error = []
                # Check if this log is an ERROR
                if error_level in line:
                    capturing = True
                    current_error.append(line)
                    # Split only first 3 spaces
                    # timestamp = first two parts
                    # level = third part
                    # message = remaining
                    parts = line.strip().split(maxsplit=3)
                    if len(parts) >= 4:
                        current_timestamp = f"{parts[date_field]} {parts[time_field]}"
                        current_level = parts[log_level_field]
                        current_message = parts[log_message_field]
                    else:
                        current_timestamp = ""
                        current_level = error_level
                        current_message = line.strip()
            else:
                # Continuation line (stack trace)
                if capturing:
                    current_error.append(line)
    # Save final ERROR block
    if capturing:
        error_logs.append(
            ErrorLog(
                timestamp=current_timestamp,
                level=current_level,
                message=current_message,
                raw_error="".join(current_error)
            )
        )
    return error_logs




if __name__ == "__main__":
    print(LOG_START_PATTERN)
    print(extract_error_logs(LOG_FILE_PATH)[0])