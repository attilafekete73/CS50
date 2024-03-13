import psycopg2
import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import ast
import pickle

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def dbexecute(query,vars=None):
    try:
        # Establish a connection
        conn = psycopg2.connect(
            user="postgres",
            password="Gerzson4Vilagmindenseg!",
            host="localhost",
            port="5432",
            database="CS50FP"
        )

        # Create a cursor
        cur = conn.cursor()

        if vars==None:
            cur.execute(query)
        else:
            cur.execute(query,vars)
        res=cur.fetchall
        dt=[]
        for row in res:
            dt.append(row)
        rndict={"len":int(len(dt)),"data":dt}
        
        
        # Process the result set
        return rndict

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Close the connection
        cur.close()
        conn.close()
