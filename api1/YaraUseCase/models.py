"""
Module that defines the tables

Created by: Jettin Joy
Created on: 06/11/2021
"""


from sqlalchemy.dialects.postgresql import JSON
from YaraUseCase import db


class YaraUseCaseAPI(db.Model):
    """
    Main API Table
    id : Primary Key (String)
    created_by : User who created the entry (String)
    updated_by : User who updated the entry (String)
    created_date_time : Created date and time (Date)
    updated_date_time : Updated date and time (Date)
    organization : Organization name (String)
    repository : Repository name (String)
    pipeline_step : Pipeline config.yml file steps (JSON)
    status : status whether the repo is complaint or not (String)
    operation : operation performed on the pipeline steps (String)
    """
    id = db.Column(db.String(64), primary_key=True, autoincrement=False)
    organization = db.Column(db.String(100), nullable=False)
    repo = db.Column(db.String(100), nullable=False)
    pipeline_steps = db.Column(JSON, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    operation = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    created_date_time = db.Column(db.String(100), nullable=False)
    updated_by = db.Column(db.String(100), nullable=False)
    updated_date_time = db.Column(db.DateTime, nullable=False)
