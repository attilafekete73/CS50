from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

personBP = Blueprint('personBP',__name__)
@personBP.route("/person/<person>", methods=["GET", "POST"])
def person(person):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        userid=session.get('user_id')
        submissions=sess.query(dbhead.Document.name,dbhead.Document.path).join(dbhead.User, dbhead.Document.userid==dbhead.User.id).filter(dbhead.User.username==person).distinct().all()
        
        print(submissions)
        return render_template("person.html",PERSONNAME=person,submissions=submissions)
    else:
        print('searched')
        term=request.form.get('search')
        #submissions=sess.query(dbhead.Document.name,dbhead.Document.path).join(dbhead.User, dbhead.Document.userid==dbhead.User.id).filter(dbhead.User.username==person).filter(dbhead.Document.name.like(f'%{term}%')).all()
        submissions=sess.query(dbhead.Document.name,dbhead.Document.path,dbhead.Document.date).join(dbhead.Docutags,dbhead.Docutags.documentid==dbhead.Document.id).join(dbhead.Tag,dbhead.Tag.id==dbhead.Docutags.tagid).join(dbhead.User,dbhead.User.id==dbhead.Document.userid).filter(dbhead.User.username==person).filter(dbhead.Tag.name.like(f'%{term}%')).distinct().all()
        return render_template("person.html",PERSONNAME=person,submissions=submissions)