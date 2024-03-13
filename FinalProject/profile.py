from flask import request,render_template,redirect, Blueprint,session,current_app
from helpers import login_required
profileBP = Blueprint('profileBP',__name__)

@profileBP.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    LoggedIn= current_app.config['LoggedIn']
    if LoggedIn==False:
        return redirect("/login")
    if request.method=="GET":
        return render_template("profile.html")
    else:
        return redirect("enroll.html")