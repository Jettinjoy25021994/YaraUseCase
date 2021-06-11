"""
Contains different endpoints and their functionality

Created by: Jettin Joy
Created on: 06/12/2021
"""


import json
import sys
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from YaraUseCase.models import YaraUseCaseAPI
from YaraUseCase import app, db


@app.route("/")
def index():
    """This endpoint can be used to check whether API is up and running"""
    data = {"Status": "API is up and running"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
