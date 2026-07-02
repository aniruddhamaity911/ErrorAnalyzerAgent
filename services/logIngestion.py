"""
logIngestion.py
This file contain methods that's extract ERROR logs from
passed log file and store it in vector store
"""

import re
from models import ErrorLog
from config import get_required_env
import const
def extract_error_logs(log_file_path: str):
    """
    Extracts complete ERROR log blocks, including stack traces.
    """
    environment_vars = get_required_env()
    pattern = environment_vars.get(const.LOG_START_PATTERN)
    date_field = environment_vars.get(const.DATE_FIELD)
    time_field = environment_vars.get(const.TIME_FIELD)
    log_level_field = environment_vars.get(const.LOG_LEVEL)
    log_message_field = environment_vars.get(const.LOG_MESSAGE)
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
                            raw_error=re.sub(r"\s+", " ","".join(current_error))
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




