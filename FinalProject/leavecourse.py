from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

leavecourseBP = Blueprint('leavecourseBP',__name__)
@leavecourseBP.route("/leavecourse/<course>", methods=["GET", "POST"])
def leavecourse(course):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        userid=session.get('user_id')
        courseid=sess.query(dbhead.Course.id).filter(dbhead.Course.coursename==course).all()
        #d=sess.delete(dbhead.USERCOURSES).where(dbhead.UserCourses.userid==userid).where(dbhead.UserCourses.courseid==courseid)
        d=dbhead.USERCOURSES.delete().where(dbhead.USERCOURSES.c.userid==userid,dbhead.USERCOURSES.c.courseid==courseid[0][0])
        with dbhead.engine.begin() as conn:
            conn.execute(d)
        #sess.execute(d)
        
        return redirect("/course/"+course)