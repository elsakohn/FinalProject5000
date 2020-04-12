"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FinalProject5000 import app
from FinalProject5000.models.LocalDataBase import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from FinalProject5000.models.QueryFormStructure import QueryFormStructure 
from FinalProject5000.models.QueryFormStructure import LoginFormStructure 
from FinalProject5000.models.QueryFormStructure import UserRegistrationFormStructure 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the register page."""
    form = UserRegistrationFormStructure(request.form)
    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""
            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)
    return render_template(
        'register.html',
        form=form, 
        title='register',
        year=datetime.now().year,
        message='Your application description page.'

    )
@app.route('/login')
def login():
    """Renders the login page."""
    return render_template(
        'login.html',
        title='login',
        year=datetime.now().year,
        message='Your application description page.'
    )






