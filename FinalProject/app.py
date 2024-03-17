from flask import Flask, Blueprint, flash, redirect, render_template, request, session
from flask_session import Session as flasksession
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import sqlalchemy as db
from sqlalchemy.orm import Session, sessionmaker, declarative_base
import dbhead
from index import indexBP
from login import loginBP 
from logout import logoutBP
from register import registerBP
from courses import courseBP
from people import personBP
from addData import addDataBP
from joincourse import joincourseBP
from leavecourse import leavecourseBP
from documents import documentBP
from downloader import downloaderBP
from search import searchBP

# Configure application
UPLOAD_FOLDER = 'C:/Users/attil/CS50/FinalProject/documents'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dbhead
sess = dbhead.Session()
User=dbhead.User
Course=dbhead.Course
UserCourses=dbhead.UserCourses


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
flasksession(app)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#index
app.register_blueprint(indexBP)

#login
app.register_blueprint(loginBP)

#logout
app.register_blueprint(logoutBP)

#register
app.register_blueprint(registerBP)
    
#courses
app.register_blueprint(courseBP)

#people
app.register_blueprint(personBP)

#addData
app.register_blueprint(addDataBP)

#joincourse
app.register_blueprint(joincourseBP)

#leavecourse
app.register_blueprint(leavecourseBP)

#document
app.register_blueprint(documentBP)

#downloader
app.register_blueprint(downloaderBP)

#search
app.register_blueprint(searchBP)
    
if __name__ == "__main__":
    app.run(debug=True)
    sess.close()