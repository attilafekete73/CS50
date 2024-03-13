from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for,send_file
from helpers import apology
from functools import wraps
import dbhead
import datetime
sess=dbhead.Session()

documentBP = Blueprint('documentBP',__name__)
@documentBP.route("/document/<doc>", methods=["GET", "POST"])
def document(doc):
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "GET":
        docid=sess.query(dbhead.Document.id).filter(dbhead.Document.name==doc).all()
        docpath=sess.query(dbhead.Document.path).filter(dbhead.Document.name==doc).all()
        filename=docpath[0][0].split("/")
        comments=sess.query(dbhead.Comment.content).filter(dbhead.Comment.documentid==docid[0][0]).order_by(dbhead.Comment.date.desc()).all()
        notedec=sess.query(dbhead.Tag.name).join(dbhead.Docutags,dbhead.Docutags.tagid==dbhead.Tag.id).join(dbhead.Document,dbhead.Document.id==dbhead.Docutags.documentid).filter(dbhead.Document.id==docid[0][0]).filter(dbhead.Tag.name=='NOTE').all()
        print(len(notedec))
        if len(notedec)==0:
            return render_template("document.html",DOCNAME=doc,comments=comments,file=filename[len(filename)-1],isnote='False')
        else:
            with open(docpath[0][0]) as f:
                contentlines = f.readlines()
                content=""
                for line in contentlines:
                    content=content+line
                return render_template("document.html",DOCNAME=doc,comments=comments,NOTE=content,isnote='True')
        #return render_template("document.html",DOCNAME=doc,comments=comments,file=filename[len(filename)-1])
    else:
        userid=session.get('user_id')
        docid=sess.query(dbhead.Document.id).filter(dbhead.Document.name==doc).all()
        docpath=sess.query(dbhead.Document.path).filter(dbhead.Document.name==doc).all()
        filename=docpath[0][0].split("/")
        new_comment=dbhead.Comment(content=request.form.get('newcomment'),date=datetime.datetime.now(),documentid=docid[0][0],userid=userid)
        sess.add(new_comment)
        sess.commit()
        comments=sess.query(dbhead.Comment.content).filter(dbhead.Comment.documentid==docid[0][0]).order_by(dbhead.Comment.date.desc()).all()
        notedec=sess.query(dbhead.Tag.name).join(dbhead.Docutags,dbhead.Docutags.tagid==dbhead.Tag.id).join(dbhead.Document,dbhead.Document.id==dbhead.Docutags.documentid).filter(dbhead.Document.id==docid[0][0]).filter(dbhead.Tag.name=='NOTE').all()
        print(len(notedec))
        print(notedec[0][0])
        if notedec[0][0] != 'NOTE':
            return render_template("document.html",DOCNAME=doc,comments=comments,file=filename[len(filename)-1],isnote='False')
        else:
            with open(filename) as f:
                contentlines = f.readlines()
                content=None
                for line in contentlines:
                    content=content+line
                return render_template("document.html",DOCNAME=doc,comments=comments,NOTE=content,isnote='True')
                