"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FinalProject5000 import app
from FinalProject5000.models.LocalDataBase import create_LocalDatabaseServiceRoutines

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from FinalProject5000.plot_service_functions import plot_to_img

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
from FinalProject5000.models.QueryFormStructure import MyForm

db_Functions = create_LocalDatabaseServiceRoutines() 
 


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
        title='About my final project',
        year=datetime.now().year,
        message=''
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
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'Login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/Query', methods=['GET', 'POST'])
def Query():

    Name = None
    Country = ''
    capital = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\קובץ נתונים בתי מלון בישראל.csv'))
    df = df.set_index('Country')

    raw_data_table = df.to_html(classes = 'table table-hover')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        Country = name
        if (name in df.index):
            capital = df.loc[name,'Capital']
            raw_data_table = ""
        else:
            capital = name + ', no such country'
        form.name.data = ''



    return render_template('Query.html', 
            form = form, 
            name = capital, 
            Country = Country,
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )

@app.route('/plot_demo' , methods = ['GET' , 'POST'])
def plot_demo():

    Form1 = MyForm(request.form)
    

    chart = ''
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\hotel v4.csv'), encoding='utf-8')
    
    x=df["Name"].tolist()
    name_choices=list(zip(x,x))

    MyForm.city_name.choices = name_choices
    if request.method == 'POST':
        level = MyForm.My.data
        name_list = MyForm.name.data
        print(name_list)
        #df-df.drop(df.index{[0]})
        df = df.drop('Name',1)
        df = df.set_index('City')
        df.index=df.index.astype(str)
        print(df)
        print(df.index.tolist())
        df = df.loc[City_list]
        print(df)
        df = df.transpose()
        print(df)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.4)
        df.plot(kind='bar',ax=ax)
        chart = plot_to_img(fig)
    df = df.groupby('City').sum()
    df = df.transpose()
    df = df.reset_index()
    df = df.tail(30)


    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(ax = ax , kind = 'bar')
    chart = plot_to_img(fig)
    
    return render_template(
        'plot_demo.html',
        img_under_construction = '/static/imgs/under_construction.png',
        chart = chart ,
        height = 300 ,
        width = 750
    )
@app.route('/DataModel')
def DataModel():
    """renders the contact page."""
    return render_template(
        'DataModel.html',
        title= 'this is the data model of hotels',
        year=datetime.now().year,
        message='this page will show you the table of hotels in israel'
        )
@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\hotel v4.csv'), encoding='utf-8')
    raw_data_table = df.to_html(classes = 'table table-hover')


    """ renders the contact page. """
    return render_template(
        'DataSet1.html',
        title ='this is the data set page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='in this page we will see the data set of the hotels'
        )






