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
            return redirect(url_for("user_dashboard",u_id=usr.id))
        elif dcr:
            return redirect(url_for("doctor_dashboard",d_id=dcr.id))
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
        if f_name and uname and pwd:
            new_user=User_Info(full_name=f_name,email=uname,password=pwd)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html",pop_up="Registration Successfully, Login now!")
        else:
            return render_template("signup.html",pop_up="Enter all details!")
    return render_template("signup.html",pop_up="")

#names
@app.route("/admin/<name>")
def admin_dashboard(name):
    doctor_list=all_doctor()
    patient_list=all_user()
    appoin=all_appointments()
    return render_template("admin_dashboard.html",usern=name,doctor_list=doctor_list,patient_list=patient_list,appointments_list=appoin,pop_up="")
@app.route("/user/<u_id>")
def user_dashboard(u_id):
    u_id = int(u_id)
    name=u_get(u_id,"name","user")
    dept=all_departments()
    usr=User_Info.query.filter_by(id=u_id).first()
    appoin=Appointments.query.filter_by(user_id=u_id).all()
    return render_template("user_dashboard.html",usern=name,department_list=dept,appointments=appoin,pop_up="",u_id=u_id,usr=usr)
@app.route("/doctor/<d_id>")
def doctor_dashboard(d_id):
    d_id = int(d_id)
    today=date.today()
    dcr=Doctor_Info.query.filter_by(id=d_id).first()
    appoin=Appointments.query.filter(Appointments.doctor_id == d_id,Appointments.date >= today).all()
    name=u_get(d_id,"name","doctor")
    return render_template("doctor_dashboard.html",usern=name,appointments_list=appoin,doct_id=d_id,dcr=dcr)

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
        elif not (f_name and uname and pwd and dept_id and experience and bio):
            return render_template("admin_add_doctor.html",pop_up="Please! Enter all details of this doctor.",usern=a_n(),department_list=dept)
        new_user=Doctor_Info(full_name=f_name,email=uname,password=pwd,dept_id=dept_id,experience=experience,bio=bio)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=a_n(),pop_up="Doctor has updated...."))
    return render_template("admin_add_doctor.html",pop_up="",usern=a_n(),department_list=dept)


@app.route("/admin_doc_update/<d_id>", methods=["GET", "POST"])
def admin_doc_update(d_id):
    dept=all_departments()
    doc=Doctor_Info.query.filter_by(id=d_id).first()
    if request.method=="POST":
        f_name=request.form.get("full_name")
        uname=request.form.get("email")
        pwd=request.form.get("password")
        dept_id=request.form.get("specialization_id")
        exp=request.form.get("experience")
        bio=request.form.get("bio")
        usr=Doctor_Info.query.filter(Doctor_Info.email==uname,Doctor_Info.id!=d_id).first()
        if usr:
            return render_template("admin_update_doct.html",pop_up="This doctor already exists... Try different email id",usern=a_n(),department_list=dept,doc=doc)
        elif not (f_name and uname and pwd and dept_id and exp and bio):
            return render_template("admin_update_doct.html",pop_up="Please! Enter all details of this doctor.",usern=a_n(),department_list=dept,doc=doc)
        
        doc.full_name=f_name
        doc.email=uname
        doc.password=pwd
        doc.dept_id=dept_id
        doc.experience=exp
        doc.bio=bio
        
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=a_n(),pop_up="Doctor has added...."))
    return render_template("admin_update_doct.html",pop_up="",usern=a_n(),department_list=dept,doc=doc)


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
        elif not (id and specialization and description):
            return render_template("admin_add_department.html",pop_up="Please! Enter all details")
        new_dept=Department(id=id,specialization=specialization,description=description)
        db.session.add(new_dept)
        db.session.commit()
        return render_template("admin_department.html",pop_up="New department has addded",usern=a_n(),department_list=all_departments())
    return render_template("admin_add_department.html",pop_up="")


@app.route("/department_details/<u_id>/<d_id>")
def department_details(u_id,d_id):
    d=Department.query.filter(Department.id==d_id).first()
    doctors=Doctor_Info.query.filter(Doctor_Info.dept_id==d_id).all()
    name=u_get(u_id,"name","user")
    return render_template("user_department_details.html",doctor_list=doctors,department=d,usern=name,u_id=u_id)

@app.route("/doc_details/<u_id>/<doc_id>/<d_id>")
def doc_details(u_id,doc_id,d_id):
    doc=Doctor_Info.query.filter(Doctor_Info.id==doc_id).first()
    dept=Department.query.filter(Department.id==d_id).first()
    name=u_get(u_id,"name","user")
    return render_template("user_doc_details.html",usern=name,doctor=doc,dept_id=d_id,department=dept,u_id=u_id)

@app.route("/doct_availability/<doc_id>", methods=["GET", "POST"])
def doct_availability(doc_id):
    doctor_id=doc_id
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
        return redirect(url_for("doctor_dashboard",d_id=doctor_id))
    #Show next 7 days
    today = date.today()
    week_days = [(today + timedelta(days=i)) for i in range(7)]
    return render_template("doct_availability.html", week_days=week_days,doct_id=doctor_id)

@app.route("/appointment_form/<doc_id>/<u_id>", methods=["GET", "POST"])
def appointment_form(doc_id,u_id):
    today=date.today()
    list=Availability.query.filter(Availability.doctor_id == doc_id,Availability.date >= today).all()
    count1=Availability.query.filter(Availability.doctor_id == doc_id,Availability.date >= today).count()
    appoin_check=Appointments.query.filter_by(user_id=u_id,doctor_id=doc_id).all()
    if request.method=="POST":
        date_str = None
        appoin_timeSlot = None
        for key in request.form.keys():
            date_str, appoin_timeSlot = key.split("_")
            break #or instead of break i can apply filter -> if "_" in key and key[0].isdigit(): 
        visit_type=request.form.get("visit_type")
        appoin_date=date.fromisoformat(date_str)
        for a in appoin_check:
            if a.date==appoin_date and a.time_slot==appoin_timeSlot:
                return render_template("user_appointment.html",count=count1,avail_list=list,doc_id=doc_id,u_id=u_id, pop_up="You Have Already An Appointment On This Slot!")
        user_appoin = Appointments(user_id=u_id,doctor_id=doc_id,date=appoin_date,time_slot=appoin_timeSlot,visit_type=visit_type)
        db.session.add(user_appoin)
        db.session.commit()
        return redirect(url_for("user_dashboard",u_id=u_id))
    return render_template("user_appointment.html",count=count1,avail_list=list,doc_id=doc_id,u_id=u_id,pop_up="")

@app.route("/apppointment_update/<appoin_id>", methods=["GET", "POST"])
def ap_update(appoin_id):
    a_p=Appointments.query.filter(Appointments.id==appoin_id).first()
    d_id=a_p.doctor_id
    if request.method=="POST":
        t=request.form.get("test_done")
        d=request.form.get("diagnosis")
        p=request.form.get("prescription")
        m=request.form.get("medicines")
        a_p.test_done=t
        a_p.diagnosis=d
        a_p.prescription=p
        a_p.medicines=m
        db.session.commit()
        return redirect(url_for("doctor_dashboard",d_id=d_id))
    return render_template("doct_update_patient_hist.html",appointment=a_p,d_id=d_id)

#All history routers
@app.route("/admin_user_hist/<u_id>/<d_id>")
def admin_user_hist(u_id,d_id):
    print("______________________",u_id,d_id)
    u_id=int(u_id)
    d_id=int(d_id)
    p_h=Appointments.query.filter_by(user_id=u_id,doctor_id=d_id).all()
    return render_template("admin_user_history.html",history_list=p_h,usern=a_n())

@app.route("/doc_user_hist/<u_id>/<d_id>")
def doc_user_hist(u_id,d_id):
    p_h=Appointments.query.filter_by(user_id=u_id,doctor_id=d_id).all()
    return render_template("doct_user_history.html",history_list=p_h,d_id=d_id)

@app.route("/user_hist/<u_id>")
def user_hist(u_id):
    u_id=int(u_id)
    name=u_get(u_id,"name","user")
    p_h=Appointments.query.filter_by(user_id=u_id).all()
    return render_template("user_history.html",usern=name,history_list=p_h,u_id=u_id)

@app.route("/edit_user_profile/<u_id>",methods=["GET", "POST"])
def edit_user_profile(u_id):
    u_p=User_Info.query.filter(User_Info.id==u_id).first()
    if request.method=="POST":
        name=request.form.get("full_name")
        em=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter(User_Info.email==em,User_Info.id!=u_id).first()
        if usr:
            return render_template("user_edit_profile.html", pop_up="This user already exists... Try different email id",u_id=u_id,user_detail=u_p)
        elif not (name and em and pwd):
            return render_template("user_edit_profile.html", pop_up="Please! Enter all details",u_id=u_id,user_detail=u_p)
        u_p.full_name=name
        u_p.email=em
        u_p.password=pwd
        db.session.commit()
        return redirect(url_for("user_dashboard",u_id=u_id))
    return render_template("user_edit_profile.html",u_id=u_id,user_detail=u_p)

@app.route("/user_appoin_cancel/<appoin_id>/<u_id>")
def user_appoin_cancel(appoin_id,u_id):
    ap = Appointments.query.filter_by(id=appoin_id).first()
    if ap:
        ap.status="Appointment is cancelled!"
        db.session.commit()

    return redirect(url_for('user_dashboard',u_id=u_id))


@app.route("/doc_appoin_status/<appoin_id>/<d_id>/<msg>")
def doc_appoin_status(appoin_id,d_id,msg):
    msg=str(msg)
    ap = Appointments.query.filter_by(id=appoin_id).first()
    if ap:
        ap.status=msg
        db.session.commit()
    return redirect(url_for("doctor_dashboard",d_id=d_id))

@app.route("/block_p/<person_id>/<who_p>")
def block_p(person_id,who_p):
    if who_p=="user":
        u=User_Info.query.filter_by(id=person_id).first()
    elif who_p=="doctor":
        u=Doctor_Info.query.filter_by(id=person_id).first()
    if u:
        u.is_blacklist=1
        db.session.commit()
    return redirect(url_for("admin_dashboard",name=a_n()))

@app.route("/unblock_p/<person_id>/<who_p>")
def unblock_p(person_id,who_p):
    if who_p=="user":
        u=User_Info.query.filter_by(id=person_id).first()
    elif who_p=="doctor":
        u=Doctor_Info.query.filter_by(id=person_id).first()
    if u:
        u.is_blacklist=0
        db.session.commit()
    return redirect(url_for("admin_dashboard",name=a_n()))

@app.route("/delete_person/<p_id>/<opertion>")
def delete_person(p_id,opertion):
    if opertion=="user":
        u=User_Info.query.filter_by(id=p_id).first()
    elif opertion=="doctor":
        u=Doctor_Info.query.filter_by(id=p_id).first()
    if u:
        db.session.delete(u)
        db.session.commit()
    return redirect(url_for("admin_dashboard",name=a_n()))

#search routers 
@app.route("/admin_search_bar/<name>",methods=["GET", "POST"])
def admin_search_bar(name):
    if request.method=="POST":
        s_txt=request.form.get("search_by_name")
        doctor_list, patient_list,appoin=a_searchbar(s_txt)
        if doctor_list or patient_list or appoin:
            return render_template("admin_dashboard.html",usern=name,doctor_list=doctor_list,patient_list=patient_list,appointments_list=appoin,pop_up="")
    return redirect(url_for("admin_dashboard",name=a_n()))


@app.route("/user_dashboard_search_bar/<u_id>",methods=["GET", "POST"])
def user_dashboard_search_bar(u_id):
    #today=date.today()
    u_id = int(u_id)
    name=u_get(u_id,"name","user")
    usr=User_Info.query.filter_by(id=u_id).first()
    #appoin=Appointments.query.filter(Appointments.user_id==u_id, Appointments.date>=today).all()
    if request.method=="POST":
        s_text=request.form.get("search_by_name")
        department_name, dept_appoin=search_department(s_text,u_id)
        #appoin_doctors_name=search_doctor_appoin(s_text,u_id)
        if department_name or dept_appoin:
            return render_template("user_dashboard.html",usern=name,department_list=department_name,appointments=dept_appoin,pop_up="",u_id=u_id,usr=usr)
        # elif appoin_doctors_name:
        #     return render_template("user_dashboard.html",usern=name,department_list=dept,appointments=appoin_doctors_name,pop_up="",u_id=u_id,usr=usr)
    return redirect(url_for("user_dashboard",u_id=u_id))


@app.route("/dept_detail_search_bar/<u_id>/<d_id>",methods=["GET", "POST"])
def dept_detail_search_bar(u_id,d_id):
    d=Department.query.filter(Department.id==d_id).first()
    doctors=Doctor_Info.query.filter(Doctor_Info.dept_id==d_id).all()
    name=u_get(u_id,"name","user")
    if request.method =="POST":
        s_txt=request.form.get("search_by_name")
        doctors_name=search_dept_doctor(s_txt,d_id) 
        return render_template("user_department_details.html",doctor_list=doctors_name,department=d,usern=name,u_id=u_id)
    return render_template("user_department_details.html",doctor_list=doctors,department=d,usern=name,u_id=u_id)

#my supported functions
def a_n():
    u = User_Info.query.filter_by(role=0).first()
    if u:
        return u.full_name
def u_n(name):
    u = User_Info.query.filter(or_(User_Info.email == name, User_Info.full_name == name)).first()
    d = Doctor_Info.query.filter(or_(Doctor_Info.email == name, Doctor_Info.full_name == name)).first()
    if u:
        return u.full_name
    elif d:
        return d.full_name
    return None
def u_get(u_id, operation,who_m):
    u = User_Info.query.filter_by(id=u_id,role=1).first()
    d = Doctor_Info.query.filter_by(id=u_id).first()
    if who_m=="doctor" and d:
        if operation == "name":
            return d.full_name
        elif operation == "email":
            return d.email
    elif who_m=="user" and u:
        if operation == "name":
            return u.full_name
        elif operation == "email":
            return u.email
    return "No name"


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


# search functions
def a_searchbar(s_txt):
    appointment=Appointments.query.join(Doctor_Info, Doctor_Info.id==Appointments.doctor_id).join(Department, Department.id==Doctor_Info.dept_id).join(User_Info, User_Info.id==Appointments.user_id).filter(or_(Department.specialization.ilike(f"%{s_txt}%"),Doctor_Info.full_name.ilike(f"%{s_txt}%"),User_Info.full_name.ilike(f"%{s_txt}%"))).all()
    user=User_Info.query.filter(or_(User_Info.full_name.ilike(f"%{s_txt}%"),User_Info.id.ilike(f"%{s_txt}%"))).all()
    doctor=Doctor_Info.query.join(Department, Department.id==Doctor_Info.dept_id).filter(or_(Doctor_Info.full_name.ilike(f"%{s_txt}%"),Department.specialization.ilike(f"%{s_txt}%"))).all()
    return doctor, user,appointment


def search_department(s_text,u_id):
    today=date.today()
    dept_name=Department.query.filter(Department.specialization.ilike(f"%{s_text}%")).all()
    dept_appointment=Appointments.query.join(Doctor_Info, Doctor_Info.id==Appointments.doctor_id).join(Department, Department.id==Doctor_Info.dept_id).filter(or_(Department.specialization.ilike(f"%{s_text}%"),Doctor_Info.full_name.ilike(f"%{s_text}%")), Appointments.date>=today,Appointments.user_id==u_id).all()
    return dept_name,dept_appointment

# def search_doctor_appoin(s_text,u_id):
#     today=date.today()
#     doctor=Appointments.query.join(Doctor_Info, Appointments.doctor_id == Doctor_Info.id).filter(Appointments.user_id==u_id,Doctor_Info.full_name.ilike(f"%{s_text}%"), Appointments.date>=today).all()
#     return doctor

def search_dept_doctor(s_txt,d_id):
    doctor=Doctor_Info.query.join(Department, Department.id == Doctor_Info.dept_id).filter(Doctor_Info.dept_id == d_id,Doctor_Info.full_name.ilike(f"%{s_txt}%")).all()
    return doctor
#search example
# def search_by_location(search_txt):
#     theatres=Theatre.query.filter(Theatre.location.ilike(f"%{search_txt}%")).all()
#     return theatres