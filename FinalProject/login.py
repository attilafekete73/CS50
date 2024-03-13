from flask import Flask, redirect, render_template, request, session, Blueprint
from helpers import apology
from werkzeug.security import check_password_hash
import dbhead

app=Flask(__name__)
sess=dbhead.Session()
User=dbhead.User
Course=dbhead.Course
UserCourses=dbhead.UserCourses

loginBP = Blueprint('loginBP',__name__)

@loginBP.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        name = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not name:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows=sess.query(User).filter_by(username=name).all()
        # Ensure username exists and password is correct
        print(len(rows))
        for row in rows:
            print(row.username)
        if len(rows) != 1 or not check_password_hash(rows[0].hash, password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0].id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
