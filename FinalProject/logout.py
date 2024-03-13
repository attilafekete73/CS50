from flask import Flask, session, redirect, Blueprint

logoutBP = Blueprint('logoutBP',__name__)

@logoutBP.route("/logout")
def logout():
    session.clear()
    return redirect("/")