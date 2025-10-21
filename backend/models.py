#Data models 
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

#first 
class User_Info(db.Model):
    __tablename__ = "user_info"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    full_name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default=1)
    appointments=db.relationship("Appointments",cascade="all,delete",backref="user_info",lazy=True)

#second
class Department(db.Model):
    __tablename__ = "department"
    id=db.Column(db.String,primary_key=True,nullable=False)
    specialization=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    doctor=db.relationship("Doctor_Info",cascade="all,delete",backref="department",lazy=True)


class Doctor_Info(db.Model):
    __tablename__ = "doctor_info"
    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    dept_id=db.Column(db.String,db.ForeignKey("department.id"),nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    bio=db.Column(db.String,nullable=False)
    appointments=db.relationship("Appointments",cascade="all,delete",backref="doctor_info",lazy=True)
    availability=db.relationship("Availability",cascade="all,delete",backref="doctor_info",lazy=True)

#third
class Appointments(db.Model):
    __tablename__ = "appointments"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    doctor_id=db.Column(db.Integer,db.ForeignKey("doctor_info.id"),nullable=False)
    date_time=db.Column(db.Integer,nullable=False)
    status=db.Column (db.String,nullable=False)
    diagnosis=db.Column(db.String,nullable=False)
    prescription=db.Column(db.String,nullable=False)
    test_done=db.Column(db.String,nullable=True)


class Availability(db.Model):
    __tablename__ = "availability"
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    doctor_id=db.Column(db.Integer,db.ForeignKey("doctor_info.id"),nullable=False)
    date=db.Column(db.Date,nullable=False)
    time_slot=db.Column(db.Time,nullable=False)
    is_booked=db.Column(db.String,nullable=False)
    
    # python
    # from backend.models import db
    # from app import *
    # db.create_all()
    # quit()