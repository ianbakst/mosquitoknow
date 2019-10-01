from flask import Flask, render_template, redirect
from flaskapp import app
from flask import request, url_for
from demo import runmodel
import matplotlib
matplotlib.use('Agg')
import datetime as dt
import numpy as np
import pandas as pd
import time

@app.route('/',methods=['GET','POST'])
def root():
    return redirect("/index")

@app.route('/index',methods=['GET','POST'])
def index():
    d0 = dt.datetime.today().date()
    today_str = str(d0)
    oneweek = str((d0 + pd.DateOffset(7)).date())
    if request.method == 'POST':
        form_data=dict(request.form)
        date_str = {'date':form_data['date1']}
        if date_str['date']=='':
            return redirect("/error")
        app.logger.info(form_data['date1'][0])
        date = pd.to_datetime(date_str['date']).date()
        fname = runmodel(date)
        return redirect(url_for('output', file = fname))
    return render_template("index.html", title = 'Mosquito Know', today = today_str, oneweek = oneweek)

@app.route('/output',methods=['GET','POST'])
def output():
    file=request.args.get('file')
    if request.method == 'POST':
        return redirect("/index")
    return render_template("output.html",title = 'Mosquito Know', file = file)

@app.route('/error',methods=['GET','POST'])
def error():
    if request.method == 'POST':
        return redirect("/index")
    return render_template("error.html", title = 'Mosquito Know')

@app.route('/about')
def about():
    return render_template("about.html", title = 'Mosquito Know')
