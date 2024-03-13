from flask import Flask,Blueprint,redirect, session, current_app,request,render_template,url_for
from helpers import apology
from functools import wraps
import dbhead

sess=dbhead.Session()

addDataredBP = Blueprint('addDataredBP',__name__)
@addDataredBP.route("/addDatared", methods=["GET", "POST"])
def addDatared():
    if session.get('user_id') is None:
        return redirect("/login")
    if request.method == "POST":
        return redirect("addData")
    