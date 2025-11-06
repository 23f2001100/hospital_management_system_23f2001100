#routers
from flask import Flask,render_template, request,url_for,redirect
from .models import *
from flask import current_app as app
from sqlalchemy import or_, and_, not_
from datetime import date, timedelta

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname, password=pwd).first()
        dcr=Doctor_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0:
            return redirect(url_for("admin_dashboard",name=a_n()))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard",name=u_n(uname)))
        elif dcr:
            return redirect(url_for("doctor_dashboard",name=u_n(uname),d_id=dcr.id))
        else:
            return render_template("login.html",pop_up="Invalid info")
    return render_template("login.html",pop_up="")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        f_name=request.form.get("full_name")
        uname=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html",pop_up="This user already exists... Try different email id")
        #user table
        new_user=User_Info(full_name=f_name,email=uname,password=pwd)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html",pop_up="Registration Successfully, Login now!")
    return render_template("signup.html",pop_up="")

#names
@app.route("/admin/<name>")
def admin_dashboard(name):
    doctor_list=all_doctor()
    patient_list=all_user()
    appointments_list=all_appointments()
    return render_template("admin_dashboard.html",usern=name,doctor_list=doctor_list,patient_list=patient_list,appointments_list=appointments_list,pop_up="")
@app.route("/user/<name>")
def user_dashboard(name):
    dept=all_departments()
    appointments=all_appointments()
    return render_template("user_dashboard.html",usern=name,department_list=dept,appointments=appointments)
@app.route("/doctor/<name>/<d_id>")
def doctor_dashboard(name,d_id):
    appoin=Appointments.query.filter(Appointments.doctor_id==d_id).all()
    return render_template("doctor_dashboard.html",usern=name,appointments_list=appoin,doct_id=d_id)

#Adding doctor
@app.route("/add_doctor",methods=["GET","POST"])
def admin_add_doctor():
    dept=all_departments()
    if request.method=="POST":
        f_name=request.form.get("full_name")
        uname=request.form.get("email")
        pwd=request.form.get("password")
        dept_id=request.form.get("specialization_id")
        experience=request.form.get("experience")
        bio=request.form.get("bio")
        usr=Doctor_Info.query.filter_by(email=uname).first()
        if usr:
            return render_template("admin_add_doctor.html",pop_up="This doctor already exists... Try different email id",usern=a_n(),department_list=dept)
        new_user=Doctor_Info(full_name=f_name,email=uname,password=pwd,dept_id=dept_id,experience=experience,bio=bio)
        db.session.add(new_user)
        db.session.commit()
        return render_template("admin_dashboard.html",usern=a_n(),doctor_list=all_doctor(),patient_list=all_user(),appointments_list=all_appointments(),pop_up="Doctor has added....")
    return render_template("admin_add_doctor.html",pop_up="",usern=a_n(),department_list=dept)

@app.route("/admin_department")
def admin_department():
    dep=all_departments()
    return render_template("admin_department.html",department_list=dep,usern=a_n(),pop_up="")
@app.route("/add_department",methods=["GET", "POST"])
def add_department():
    if request.method=="POST":
        id=request.form.get("id")
        specialization=request.form.get("specialization")
        description=request.form.get("description")
        dept=Department.query.filter_by(specialization=specialization).first()
        if dept:
            return render_template("admin_add_department.html",pop_up="This is already exist")
        new_dept=Department(id=id,specialization=specialization,description=description)
        db.session.add(new_dept)
        db.session.commit()
        return render_template("admin_department.html",pop_up="New department has addded",usern=a_n(),department_list=all_departments())
    return render_template("admin_add_department.html",pop_up="")

@app.route("/department_details/<name>/<d_id>")
def department_details(name,d_id):
    d=Department.query.filter(Department.id==d_id).first()
    doctors=Doctor_Info.query.filter(Doctor_Info.dept_id==d_id).all()
    return render_template("user_department_details.html",doctor_list=doctors,department=d,usern=name)

@app.route("/doc_details/<name>/<doc_id>/<d_id>")
def doc_details(name,doc_id,d_id):
    doc=Doctor_Info.query.filter(Doctor_Info.id==doc_id).first()
    dept=Department.query.filter(Department.id==d_id).first()
    return render_template("user_doc_details.html",usern=name,doctor=doc,dept_id=d_id,department=dept)

@app.route("/doct_availability/<doc_id>", methods=["GET", "POST"])
def doct_availability(doc_id):
    doctor_id=doc_id
    doc=Doctor_Info.query.filter_by(id=doctor_id).first()
    doc_name=doc.full_name
    if request.method == "POST":
        selected_slots = request.form
        Availability.query.filter_by(doctor_id=doctor_id).delete()
        today = date.today()
        for i in range(7):
            day = today + timedelta(days=i)
            for period in ["morning", "evening"]:
                key = f"{day}_{period}"
                is_available = key in selected_slots
                new_slot = Availability(
                    doctor_id=doc_id,
                    date=day,
                    time_slot=period,
                    is_present=True if is_available else False
                )
                db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for("doctor_dashboard",name=doc_name,d_id=doctor_id))
    #Show next 7 days
    today = date.today()
    week_days = [(today + timedelta(days=i)) for i in range(7)]
    return render_template("doct_availability.html", week_days=week_days,doct_id=doctor_id)

@app.route("/appointment_form/<doc_id>/<user_id>")
def appointment_form(doc_id,user_id):
    print("-----------------",request.method,"----------")
    avail_list=Availability.query.filter_by(doctor_id=doc_id).all()
    return render_template("appointment.html",avail_list=avail_list,doc_id=doc_id,user_id=user_id)

# @app.route("/user_history/<id>/<department>")
# def user_history(pid,department):
#     appointments=all_appointments()
#     p=Patient_Info.query.filter_by(id=pid).first()
#     return render_template("user_history",id=pid,p_deatils=p,department=department,appointments=appointments,patient_list=all_user())




#my functions
def a_n():
    u=User_Info.query.all()
    return u[0].full_name
def u_n(name):
    u = User_Info.query.filter(or_(User_Info.email == name, User_Info.full_name == name)).first()
    d = Doctor_Info.query.filter(or_(Doctor_Info.email == name, Doctor_Info.full_name == name)).first()
    if u:
        return u.full_name
    elif d:
        return d.full_name
    return None
def all_doctor():
    doctor=Doctor_Info.query.all()
    return doctor
def all_user():
    patient=User_Info.query.filter(User_Info.role==1).all()
    return patient
def all_appointments():
    appointments=Appointments.query.all()
    return appointments
def all_departments():
    dept=Department.query.all()
    return dept