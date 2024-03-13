from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for,send_from_directory
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

UPLOAD_FOLDER = 'C:/Users/attil/CS50/FinalProject/documents'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
downloaderBP = Blueprint('downloaderBP',__name__)
@downloaderBP.route('/downloader/<filename>')
def downloader(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)