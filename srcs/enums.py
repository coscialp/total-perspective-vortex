"""
This module contains all utility functions and classes for the project.
"""

from enum import Enum
from typing import List

from srcs.errors import ValidationError


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


class TaskEnum(Enum):
    """
    Enum to define the task type

    Attributes:
        Task1: Task 1. values: [3, 7, 11]
        Task2: Task 2. values: [4, 8, 12]
        Task3: Task 3. values: [5, 9, 13]
        Task4: Task 4. values: [6, 10, 14]`

    """

    Task1 = [3, 7, 11]
    Task2 = [4, 8, 12]
    Task3 = [5, 9, 13]
    Task4 = [6, 10, 14]

    @staticmethod
    def range():
        """
        Get the range of task values

        Returns:
            tuple: Minimum and maximum task values
        """
        return 1, len(TaskEnum.all())

    @staticmethod
    def get(index: int) -> List[int]:
        """
        Get the task type

        Args:
            index (int): Task number corresponding to the task type (1<=index<=len(TaskEnum.all()))

        Returns:
            TaskEnum: Task type
        """
        try:
            return TaskEnum.all()[index - 1]
        except IndexError:
            raise ValidationError("task", str(range(len(TaskEnum.all()))), f"{index}")

    @staticmethod
    def all():
        return [task.value for task in TaskEnum]
