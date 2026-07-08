"""
SQLAlchemy models for OptiCrop.

Five tables map the core of the project ER diagram:
    User        -> User
    SoilData    -> SoilData        (the 7 soil/climate inputs a user submits)
    Crop        -> Crop            (reference table, seeded with 22 crops)
    MLModel     -> MLModel         (metadata about the deployed model)
    Prediction  -> Prediction      (a recommendation, links SoilData + MLModel + Crop)

The ER "Dataset" and "Report" entities are represented without dedicated
tables: Dataset = dataset/Crop_recommendation.csv + MLModel.model_file,
Report  = the result / history views.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Farmer')

    soil_data = db.relationship('SoilData', backref='user', lazy=True)


class SoilData(db.Model):
    __tablename__ = 'soil_data'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prediction = db.relationship('Prediction', backref='soil_data', uselist=False, lazy=True)


class Crop(db.Model):
    __tablename__ = 'crop'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(50), unique=True, nullable=False)
    crop_type = db.Column(db.String(50))
    season = db.Column(db.String(50))
    optimal_ph = db.Column(db.String(30))
    water_requirement = db.Column(db.String(30))
    tips = db.Column(db.String(300))

    predictions = db.relationship('Prediction', backref='crop', lazy=True)


class MLModel(db.Model):
    __tablename__ = 'ml_model'

    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    algorithm_type = db.Column(db.String(100), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    model_file = db.Column(db.String(200), nullable=False)

    predictions = db.relationship('Prediction', backref='ml_model', lazy=True)


class Prediction(db.Model):
    __tablename__ = 'prediction'

    id = db.Column(db.Integer, primary_key=True)
    soil_id = db.Column(db.Integer, db.ForeignKey('soil_data.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('ml_model.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=True)
    recommended_crop = db.Column(db.String(50), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
