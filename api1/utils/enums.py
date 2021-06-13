"""
Holds constant values

Created By: Jettin Joy
Created on: 06/12/2021
"""


from enum import Enum


class Status(Enum):
    """Enum to hold the values for status of the repository"""
    complaint_status = "COMPLAINT"
    non_complaint_status = "NON-COMPLAINT"
    pending_status = "PENDING"
    verified_status_no = "NO"
    verified_status_yes = "YES"
    outdated_status_no = "NO"
    outdated_status_yes = "YES"


class Operation(Enum):
    """Enum to hold values for different operation on config"""
    create = "CREATE"
    update = "UPDATE"
    delete = "DELETE"


class StatConf(Enum):
    """Enums to hold constant conf formats"""
    date_format = '%Y-%m-%d %H:%M:%S'
