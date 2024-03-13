from flask import Flask,Blueprint,redirect, session, current_app,request,render_template
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

indexBP = Blueprint('indexBP',__name__)
@indexBP.route("/", methods=["GET", "POST"])
def index():
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        userid=session.get('user_id')
        courses = sess.query(dbhead.Course.coursename).join(dbhead.UserCourses, dbhead.UserCourses.courseid==dbhead.Course.id).join(dbhead.User,dbhead.User.id==dbhead.UserCourses.userid).filter(dbhead.User.id==userid).distinct(dbhead.Course.id)
        #last 10 notif. categories: document in course, comment to your doc
        docincourse = sess.query(dbhead.Document.name, dbhead.Course.coursename).join(dbhead.Course,dbhead.Course.id==dbhead.Document.courseid).filter(dbhead.Course.coursename.in_(courses)).order_by(dbhead.Document.date.desc()).limit(10)
        commenttodoc = sess.query(dbhead.Document.name, dbhead.User.username, dbhead.Comment.content).join(dbhead.Comment, dbhead.Comment.documentid==dbhead.Document.id).join(dbhead.User, dbhead.User.id==dbhead.Document.userid).where(dbhead.Document.userid==userid).order_by(dbhead.Comment.date.desc()).limit(10)
        return render_template("/index.html",table=courses, docincourse=docincourse, commenttodoc=commenttodoc)