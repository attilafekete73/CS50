from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead
import os
import datetime

sess=dbhead.Session()
UPLOAD_FOLDER = 'C:/Users/attil/CS50/FinalProject/documents'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'mp4', 'mp3', 'doc', 'docx', 'epub', 'mobi', 'ppt', 'pptx', 'xlsx'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

addDataBP = Blueprint('addDataBP',__name__)
@addDataBP.route("/addData/<course>", methods=["GET", "POST"])
def addData(course):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "POST":
        userid=session.get('user_id')
        courseid=sess.query(dbhead.Course.id).filter(dbhead.Course.coursename==course).all()
        nameofsubm=request.form.get("nameofsubm")
        teachername=request.form.get("teacher_name")
        try:
            note=request.form.get("note")
        except KeyError:
            note=''            
        tags=request.form.get("tags")
        taglist=tags.split(",")
        taglist.append(nameofsubm)
        taglist.append(teachername)
        if note != '':
            with open('C:/Users/attil/CS50/FinalProject/documents/'+nameofsubm+'.txt','w') as f:
                f.write(note)
            new_document=dbhead.Document(path=UPLOAD_FOLDER+'/'+nameofsubm+'.txt',name=nameofsubm,date=datetime.datetime.now(),courseid=courseid[0][0],userid=userid)
            sess.add(new_document)
            sess.commit()
            taglist.append('NOTE')
        try:
            file=request.files['file']
        except KeyError:
            file=''
        if file!='' and allowed_file(file.filename):
            print("ALLOWED")
            #file.save(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_document=dbhead.Document(path=UPLOAD_FOLDER+'/'+file.filename,name=nameofsubm,date=datetime.datetime.now(),courseid=courseid[0][0],userid=userid)
            sess.add(new_document)
            sess.commit()
            extension=file.filename.split('.')
            taglist.append(str(extension[1]))
            taglist.append(str(extension[0]))
        for tag in taglist:
            tagchecker=sess.query(dbhead.Tag.name).filter(dbhead.Tag.name==tag).all()
            if len(tagchecker)==0:
                new_tag=dbhead.Tag(name=tag)
                sess.add(new_tag)
                sess.commit()
            tagid=sess.query(dbhead.Tag.id).filter(dbhead.Tag.name==tag).all()
            documentid=sess.query(dbhead.Document.id).filter(dbhead.Document.name==nameofsubm).all()
            new_docutag=dbhead.Docutags(documentid=documentid[0][0],tagid=tagid[0][0])
            sess.add(new_docutag)
            sess.commit()
        return redirect("/course/"+course)
    else:  
        return render_template("addData.html",COURSENAME=course)
    