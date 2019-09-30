from flask import Flask, render_template, redirect
from flaskapp import app
from flask import request
from demo import runmodel
import matplotlib
matplotlib.use('Agg')
import datetime
import numpy as np
import pandas as pd
import time

@app.route('/',methods=['GET','POST'])
def root():
    return redirect("/index")

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        form_data=dict(request.form)
        date_str = {'date':form_data['date1']}
        if date_str['date']=='':
            return redirect("/error")
        app.logger.info(form_data['date1'][0])
        date = pd.to_datetime(date_str['date']).date()
        print(date)
        deltatime = (date - date.today()).total_seconds()
        if (deltatime >= 604800.0):
            return redirect("/error")
        runmodel(date)
        return redirect("/output")
    return render_template("index.html", title = 'Mosquito Know')

@app.route('/output',methods=['GET','POST'])
def output():
    if request.method == 'POST':
        return redirect("/index")
    return render_template("output.html",title = 'Mosquito Know')

@app.route('/error',methods=['GET','POST'])
def error():
    if request.method == 'POST':
        return redirect("/index")
    return render_template("error.html", title = 'Mosquito Know')
