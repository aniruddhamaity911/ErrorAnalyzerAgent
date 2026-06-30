"""
Error.py
This is data class of ERROR
representation
"""

from dataclasses import dataclass

@dataclass
class ErrorLog:
    timestamp: str
    level: str
    message: str
    raw_error: str
