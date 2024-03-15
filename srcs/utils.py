"""
This module contains all utility functions and classes for the project.
"""

from enum import Enum


class VerboseType(Enum):
    """
    Enum to define the verbose type

    Attributes:
        INFO: Information
        WARNING: Warning
        ERROR: Error
        DEBUG: Debug
        CRITICAL: Critical
    """

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"
