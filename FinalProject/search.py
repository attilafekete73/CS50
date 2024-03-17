from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead
import sqlalchemy

Document=dbhead.Document
Tag=dbhead.Tag
Docutags=dbhead.Docutags
Course=dbhead.Course
User=dbhead.User
Usercourses=dbhead.UserCourses
Comment=dbhead.Comment


sess=dbhead.Session()

searchBP = Blueprint('searchBP',__name__)
@searchBP.route("/search", methods=["GET", "POST"])
def search():
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "POST":
        filter=request.form.getlist('searchbox')
        term=request.form.get('search')
        tagres=sess.query(Document.path,Document.name,Document.date).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Tag.name.like(f'%{term}%')).distinct().all()
        courseres=sess.query(Course.coursename).filter(Course.coursename.like(f'%{term}%')).all()
        userres=sess.query(User.username).filter(User.username.like(f'%{term}%')).all()
        docres=[]
        if len(filter)==0:
            for doc in tagres:
                docres.append(doc)
            return render_template('search.html',docres=docres,courseres=courseres,userres=userres)
        if len(filter)!=0:
            #tagsearchterm=sqlalchemy.text(f"SELECT documents.path, documents.name, documents.date FROM documents JOIN docutags ON docutags.documentid=documents.id JOIN tags ON tags.id=docutags.tagid WHERE tags.name LIKE '%{term}%'")
            #if 'PICTURE' in filter or 'DOCUMENT' in filter or 'PPT' in filter or 'VIDEO' in filter or 'AUDIO' in filter
            if 'PICTURE' in filter:
                for doc in tagres:
                    tags=sess.query(Tag.name).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Document.name==doc[1]).distinct().all()
                    if 'png' in tags[0] or 'jpg' in tags[0] or 'jpeg' in tags[0]:
                        docres.append(doc)
            if 'DOCUMENT' in filter:
                for doc in tagres:
                    tags=sess.query(Tag.name).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Document.name==doc[2]).distinct().all()
                    if 'txt' in tags[0] or 'pdf' in tags[0] or 'doc' in tags[0] or 'docx' in tags[0] or 'epub' in tags[0] or 'mobi' in tags[0] or 'xlsx' in tags[0]:
                        docres.append(doc)
            if 'PPT' in filter:
                for doc in tagres:
                    tags=sess.query(Tag.name).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Document.name==doc[2]).distinct().all()
                    if 'ppt' in tags[0] or 'pptx' in tags[0]:
                        docres.append(doc)
            if 'VIDEO' in filter:
                for doc in tagres:
                    tags=sess.query(Tag.name).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Document.name==doc[2]).distinct().all()
                    if 'mp4' in tags[0]:
                        docres.append(doc)
            if 'AUDIO' in filter:
                for doc in tagres:
                    tags=sess.query(Tag.name).join(Docutags,Docutags.documentid==Document.id).join(Tag,Tag.id==Docutags.tagid).filter(Document.name==doc[2]).distinct().all()
                    if 'mp3' in tags[0]:
                        docres.append(doc)
            if len(filter)==1:
                if filter[0]=='USER':
                    return render_template('search.html',userres=userres)
                if filter[0]=='COURSE':
                    return render_template('search.html',courseres=courseres)
                else:
                    return render_template('search.html',docres=docres)
            if 'COURSE' not in filter and 'USER' not in filter:
                return render_template('search.html',docres=docres)
            if 'COURSE' not in filter:
                return render_template('search.html',docres=docres,userres=userres)
            if 'USER' not in filter:
                return render_template('search.html',docres=docres,courseres=courseres)
            if 'USER' in filter and 'COURSE' in filter and len(filter)==2:
                return render_template('search.html',courseres=courseres,userres=userres)
            else:
                return render_template('search.html',docres=docres,courseres=courseres,userres=userres)
                
        #return render_template('apology.html',top='400',bottom="search")
    