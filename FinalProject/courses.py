from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

courseBP = Blueprint('courseBP',__name__)
@courseBP.route("/course/<course>", methods=["GET", "POST"])
def course(course):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        userid=session.get('user_id')
        ismember=1
        memberdecider=sess.query(dbhead.Course).join(dbhead.UserCourses,dbhead.UserCourses.courseid==dbhead.Course.id).join(dbhead.User,dbhead.User.id==dbhead.UserCourses.userid).filter(dbhead.User.id==userid).filter(dbhead.Course.coursename==course).distinct().all()
        print(memberdecider)
        if len(memberdecider)==0:
            ismember=0
        submissions=sess.query(dbhead.Document.name,dbhead.Document.path).join(dbhead.Course, dbhead.Document.courseid==dbhead.Course.id).filter(dbhead.Course.coursename==course).distinct().all()
        
        print(submissions)
        print(ismember)
        return render_template("course.html",COURSENAME=course,member=ismember,submissions=submissions)
    else:
        print('searched')
        userid=session.get('user_id')
        term=request.form.get('search')
        submissions=sess.query(dbhead.Document.name,dbhead.Document.path,dbhead.Document.date).join(dbhead.Docutags,dbhead.Docutags.documentid==dbhead.Document.id).join(dbhead.Tag,dbhead.Tag.id==dbhead.Docutags.tagid).join(dbhead.Course,dbhead.Course.id==dbhead.Document.courseid).filter(dbhead.Course.coursename==course).filter(dbhead.Tag.name.like(f'%{term}%')).distinct().all()
        ismember=1
        memberdecider=sess.query(dbhead.Course).join(dbhead.UserCourses,dbhead.UserCourses.courseid==dbhead.Course.id).join(dbhead.User,dbhead.User.id==dbhead.UserCourses.userid).filter(dbhead.User.id==userid).filter(dbhead.Course.coursename==course).all()
        print(memberdecider)
        if len(memberdecider)==0:
            ismember=0
        return render_template("course.html",COURSENAME=course,member=ismember,submissions=submissions)