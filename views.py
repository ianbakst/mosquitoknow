from flask import Flask, render_template, redirect
from flaskapp import app
from flask import request
from demo import runmodel
import matplotlib
matplotlib.use('Agg')

@app.route('/',methods=['GET','POST'])
def root():
    return redirect("/index")
@app.route('/index',methods=['GET','POST'])
def index():
    user = { 'nickname': 'NAME' } # fake user
    if request.method == 'POST':
        form_data=dict(request.form)
        date = {'date':form_data['date1'][0]}
        app.logger.info(form_data['date1'][0])
        runmodel(date)
        return redirect("/output")
    return render_template("index.html", title = 'Skeet-Aware', user = user)

@app.route('/output',methods=['GET','POST'])
def output():
    if request.method == 'POST':
        return redirect("/index")
    return render_template("output.html")
