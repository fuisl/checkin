from flask import Flask, flash, redirect, render_template, request, session, url_for, Response
from helper import login_required, apology
from logging import FileHandler, WARNING 
from flask_session import Session 
from werkzeug.security import check_password_hash, generate_password_hash
# from camera import WebCam
# import server

import os
import flask 
import csv 
import pandas as pd 

# Update directory 
os.chdir(os.path.dirname(__file__)) 

# Configure application
app = Flask(__name__, template_folder="templates") 

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.update(SECRET_KEY=os.urandom(24))
app.config.from_object(__name__) 

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response 

@app.route("/", methods=["GET", "POST"])
def index(): 

    genders = ["Male", "Female", "Other"]
    types = ["STANDARD", "VIP"] 

    # Branching on method
    if request.method == "POST": 

        if request.form.get("face") == "yes": 
            return redirect("/camera")

        else: 
            return redirect("/view")

    else: 
        return render_template("home.html")

@app.route("/view", methods=["GET"])
def view(): 

    return render_template("view.html")

@app.route("/camera", methods=["GET"])
def camera(): 

    return render_template("camera.html") 