"""
A helper module that contains various helper functions

Created By: Jettin Joy
Created on: 06/12/2021
"""


import uuid
from datetime import datetime
from utils.enums import Operation, Status, StatConf


def format_create_config(request_data: dict):
    """Creates formatted data to be posted into API
    Parameters:
        request_data (dict): data received through request
    Returns:
        formatted_data (dict): Formatted data
    """
    formatted_data = {
        "id": str(uuid.uuid4()),
        "organization": request_data.get('organization'),
        "repo": request_data.get('repository'),
        "pipeline_steps": request_data.get('config'),
        "status": Status.pending_status.value,
        "operation": Operation.create.value,
        "created_by": request_data.get('user'),
        "created_date_time": datetime.now().strftime(
            StatConf.date_format.value
            ),
        "updated_by": request_data.get('user'),
        "updated_date_time": datetime.now().strftime(
            StatConf.date_format.value
            )
    }
    return formatted_data
