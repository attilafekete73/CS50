from flask import Flask, session, request,render_template,Blueprint
from werkzeug.security import generate_password_hash
from helpers import apology
import dbhead

sess=dbhead.Session()
User=dbhead.User
Course=dbhead.Course
UserCourses=dbhead.UserCourses
registerBP = Blueprint('registerBP',__name__)

@registerBP.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        """check if all fields contain something, check the passwords, insert the new user into users"""
        name = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        checker=sess.query(User).filter_by(username=name).all()
        #checker=checker.fetchall()
        if not name:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirm:
            return apology("must confirm password", 400)
        elif confirm != password:
            return apology("passwords doesn't match", 400)
        elif len(checker)!=0:
            return apology("username already exists", 400)
        else:
            new_user=User(username=name,hash=generate_password_hash(password))
            sess.add(new_user)
            sess.commit()
            return render_template("login.html")
    else:
        return render_template("register.html")