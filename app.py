from flask import Flask
from backend.models import db
from backend.api_controllers import *


app=None
def setup_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///hospital_management_app.sqlite3"
    
    #sql conn
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()
    app.debug=True
    print("Hospital management app is starting.....")

#calling set up
setup_app()

from backend.controllers import *
if __name__=="__main__":
    app.run()