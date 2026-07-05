"""
logIngestion.py
This file contains methods that extract ERROR logs from
the passed log file and store them in the vector store.
"""

import re

import const
from config import get_required_env
from models import ErrorLog


def extract_error_logs(log_file_path: str) -> list[ErrorLog]:
    """
    Extract complete ERROR log blocks including stack traces.
    """

    environment_vars = get_required_env()

    pattern = re.compile(environment_vars[const.LOG_START_PATTERN])

    date_field = int(environment_vars[const.DATE_FIELD])
    time_field = int(environment_vars[const.TIME_FIELD])
    log_level_field = int(environment_vars[const.LOG_LEVEL])
    log_message_field = int(environment_vars[const.LOG_MESSAGE])

    capturing = False
    current_error: list[str] = []

    error_level = "ERROR"

    current_timestamp = ""
    current_level = ""
    current_message = ""

    error_logs: list[ErrorLog] = []

    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:

            # New log entry
            if pattern.match(line):

                # Save previous error block
                if capturing:
                    error_logs.append(
                        ErrorLog(
                            timestamp=current_timestamp,
                            level=current_level,
                            message=current_message,
                            raw_error=re.sub(
                                r"\s+",
                                " ",
                                "".join(current_error)
                            ),
                        )
                    )

                    capturing = False
                    current_error = []

                # Check if current log is ERROR
                if error_level in line:
                    capturing = True
                    current_error.append(line)

                    parts = line.strip().split(maxsplit=3)

                    if len(parts) >= 4:
                        current_timestamp = (
                            f"{parts[date_field]} {parts[time_field]}"
                        )
                        current_level = parts[log_level_field]
                        current_message = parts[log_message_field]
                    else:
                        current_timestamp = ""
                        current_level = error_level
                        current_message = line.strip()

            # Stack trace / continuation
            elif capturing:
                current_error.append(line)

    # Save last error block
    if capturing:
        error_logs.append(
            ErrorLog(
                timestamp=current_timestamp,
                level=current_level,
                message=current_message,
                raw_error=re.sub(
                    r"\s+",
                    " ",
                    "".join(current_error),
                ),
            )
        )

    return error_logs