"""
Contains different endpoints and their functionality

Created by: Jettin Joy
Created on: 06/12/2021
"""


import json
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from utils.helper_util import format_create_config
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


@app.route("/create", methods=['POST'])
def create_pipeline_steps():
    """Create a CircleCI configuration for the specified repo
    Parameters:
        organization (string): Organization name in which repo
                               is associated with
        repo (string): Repository for which configuration to be generated
    Returns:
        config_steps (dict): The configuration steps for the repo in
    """
    status = {}
    if request.method == 'POST':
        try:
            created_data = YaraUseCaseAPI(
                **format_create_config(request.get_json())
                )
            db.session.add(created_data)
            db.session.commit()
            status = jsonify({"Status": "Created data successfully"}), 201
        except (KeyError, SQLAlchemyError) as err:
            db.session.rollback()
            status = jsonify({"Status": "Operation cannot be completed"}), 500
            print(str(err))
    return status
