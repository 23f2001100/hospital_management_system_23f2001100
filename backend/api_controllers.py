from flask_restful import Resource, Api
from flask import request
from .models import *

api=Api()

class DoctorApi(Resource):

    def get(self):
        doctors=Doctor_Info.query.all()
        doctors_json=[]
        for doctor in doctors:
            doctors_json.append({'id':doctor.id,'full_name':doctor.full_name,'email':doctor.email,'password':doctor.password,'dept_id':doctor.dept_id,'experience':doctor.experience,'bio':doctor.bio,'is_blacklist':doctor.is_blacklist})

        return doctors_json


    def post(self):
        full_name=request.json.get("full_name")
        email=request.json.get("email")
        password=request.json.get("password")
        dept_id=request.json.get("dept_id")
        experience=request.json.get("experience")
        bio=request.json.get("bio")
        is_blacklist=request.json.get("is_blacklist")
        new_doctor=Doctor_Info(full_name=full_name,email=email,password=password,dept_id=dept_id,experience=experience,bio=bio,is_blacklist=is_blacklist)
        db.session.add(new_doctor)
        db.session.commit()
        return {"message":"New Doctor Has Added"},201
    


    def put(self,d_id):
        doc=Doctor_Info.query.filter_by(id=d_id).first()
        if doc:
            doc.full_name=request.json.get("full_name")
            doc.email=request.json.get("email")
            doc.password=request.json.get("password")
            doc.dept_id=request.json.get("dept_id")
            doc.experience=request.json.get("experience")
            doc.bio=request.json.get("bio")
            db.session.commit()
            doc.is_blacklist=request.json.get("is_blacklist")
            return {"message": "Doctor Detail Are Updated"},200
        return {"message": "Doctor Details Are Found!. Your ID May Be Incorrect."},404

    def delete(self,d_id):
        doc=Doctor_Info.query.filter_by(id=d_id).first()
        if doc:
            db.session.delete(doc)
            db.session.commit()
            return {"message": "Doctor Detail Are Deleted"},200
        return {"message": "Doctor Details Are Found!. Your ID May Be Incorrect."},404

class Single_Doctor_detailsApi(Resource):
    def get(self,d_id):
        doctor=Doctor_Info.query.filter_by(id=d_id).first()
        if doctor:
            doctor_json=[]
            doctor_json.append({'id':doctor.id,'full_name':doctor.full_name,'email':doctor.email,'password':doctor.password,'dept_id':doctor.dept_id,'experience':doctor.experience,'bio':doctor.bio,'is_blacklist':doctor.is_blacklist})
            return doctor_json
        return {"message": "Doctor Details Are Found!. Your ID May Be Incorrect."},404
    
api.add_resource(DoctorApi,"/api/get_doctors","/api/add_doctor","/api/edit_doctor_detail/<d_id>","/api/delete_doctor/<d_id>")
api.add_resource(Single_Doctor_detailsApi,"/api/single_doc_detail/<d_id>")