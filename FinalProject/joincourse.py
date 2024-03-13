from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

joincourseBP = Blueprint('joincourseBP',__name__)
@joincourseBP.route("/joincourse/<course>", methods=["GET", "POST"])
def joincourse(course):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        userid=session.get('user_id')
        courseid=sess.query(dbhead.Course.id).filter(dbhead.Course.coursename==course).all()
        new_usercourse=dbhead.UserCourses(userid=userid,courseid=courseid[0][0])
        sess.add(new_usercourse)
        sess.commit()
        
        return redirect("/course/"+course)