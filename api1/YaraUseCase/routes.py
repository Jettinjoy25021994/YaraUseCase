"""
Contains different endpoints and their functionality

Created by: Jettin Joy
Created on: 06/12/2021
"""


import json
import uuid
from flask import jsonify, request
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from utils.helper_util import format_create_config
from YaraUseCase.models import YaraUseCaseAPI, Steps
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


@app.route("/retrieve/all", methods=['GET'])
def retrieve():
    """Retrieve the config data for all the repo in organization"""
    try:
        
        result_set = YaraUseCaseAPI.query.filter_by(outdated="NO",
                                        verified="NO", status="PENDING").all()
        output_result_set = list()
        for result in result_set:
            r_dict = dict()
            r_dict["organizarion"] = result.organization
            r_dict['repository'] = result.repo
            r_dict['conf'] = result.pipeline_steps
            r_dict['udated_date_time'] = result.updated_date_time
            r_dict['created_date_time'] = result.created_date_time
            r_dict['created_by'] = result.created_by
            r_dict['updated_by'] = result.updated_by
            r_dict['status'] = result.status
            output_result_set.append(r_dict)
        return jsonify({"All Repo details": output_result_set}),200
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        print(str(e_rr))
        return jsonify({"Status": "Something went wrong"}),500

@app.route("/retrieve/<repo>")
def retrieve_repo(repo):
    """Retrieve conf for a repo"""
    try:
        result_set = YaraUseCaseAPI.query.filter_by(outdated="NO", 
                                            repo=repo, verified="NO", status="PENDING").first()
        return jsonify({
            "organization": result_set.organization,
            "conf": result_set.pipeline_steps,
            "status": result_set.status,
            "created_by": result_set.created_by,
            "updated_by": result_set.updated_by,
        })
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        print(str(e_rr))
        return jsonify({"Status":"Conf not found for the repo"}), 404


@app.route("/update/<repo>", methods=["PUT"])
def update_repo_conf(repo):
    """Update conf for a repo"""
    try:
        existing_conf = YaraUseCaseAPI.query.filter_by(outdated="NO",
                            repo=repo).order_by(YaraUseCaseAPI.updated_date_time.desc()).first()
        existing_conf.conf = request.get_json().get('conf')
        existing_conf.updated_by  = request.get_json().get('user')
        existing_conf.updated_date_time = datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        existing_conf.status = "PENDING"
        existing_conf.verified = "NO"
        db.session.commit()
        return jsonify({"Status": "Updated Successfullt"}), 201
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        db.session.rollback()
        return jsonify({"Status": "Error Occured", "code": str(e_rr)}), 500


@app.route("/delete/<repo>", methods=["DELETE"])
def delete_repo_conf(repo):
    """Delete the conf for the repo"""
    try:
        YaraUseCaseAPI.query.filter_by(outdated="NO",
                            repo=repo).delete(synchronize_session='fetch')
        db.session.commit()
        return jsonify({"Status": "Deletion Completed"}), 201
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        db.session.rollback()
        return jsonify({"Status": "Error occured", "Code": str(e_rr)}), 500


@app.route("/statupdate/<repo>", methods=["PATCH"])
def patch_repo(repo):
    """Patch the repo details"""
    try:
        existing_conf = YaraUseCaseAPI.query.filter_by(outdated="NO",
                            repo=repo,
                            verified="NO", status="PENDING").order_by(YaraUseCaseAPI.updated_date_time.desc()).first()
        existing_conf.outdated = "YES"
        existing_conf.verfied = "YES"
        existing_conf.status = request.get_json().get('Status')
        existing_conf.updated_by = request.get_json().get('user')
        existing_conf.updated_date_time = datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        db.session.commit()
        return jsonify({"Status": "Success"}), 201
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        db.session.rollback()
        return jsonify({"Status": "Error occured", "Code": str(e_rr)}), 500

@app.route("/steps", methods=["POST"])
def get_mand_steps():
    """get the mandatory steps for check"""
    try:
        data = request.get_json()
        print(data)
        steps = data.get('steps')
        id = str(uuid.uuid4())
        steps = {"MandSteps": steps}
        c_date_time = datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        m_steps = Steps(id=id, mand_steps = steps, created_date_time=c_date_time)
        db.session.add(m_steps)
        db.session.commit()
        return jsonify({"Status": "Success"}), 201
    except (AttributeError, KeyError) as e_rr:
        db.session.rollback()
        return jsonify({"Status": str(e_rr)}), 500

@app.route('/getsteps')
def retrieve_mand_steps():
    """retrieve the mandatory steps for a repo"""
    try:
        m_steps = Steps.query.filter().order_by(Steps.created_date_time.desc()).first()
        steps = m_steps.mand_steps
        return jsonify(steps), 200
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        return {"Status": str(e_rr)}, 404

@app.route('/report')
def get_repo_report():
    """Get the repos report"""
    try:
        result_set = YaraUseCaseAPI.query.filter(YaraUseCaseAPI.status.in_(("COMPLAINT", 
                                                                                "NON-COMPLAINT"))).order_by(YaraUseCaseAPI.updated_date_time.desc()).all()
        output_result_set = []
        for result in result_set:
            r_dict = dict()
            r_dict['repo'] = result.repo
            r_dict['status'] = result.status
            output_result_set.append(r_dict)
        return jsonify({"Repo Report": output_result_set}),200
    except (AttributeError, KeyError, SQLAlchemyError) as e_rr:
        return jsonify({"Status": str(e_rr)}), 404
