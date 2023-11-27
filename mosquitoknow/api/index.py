import datetime as dt

from flask import make_response, render_template, redirect
from flask import request, url_for
import pandas as pd

from mosquitoknow.demo import runmodel


def today_str():
    return str(dt.datetime.today().date())


def one_week():
    return str((dt.datetime.today().date() + pd.DateOffset(7)).date())


def post():
    form_data = dict(request.form)
    date_str = {"date": form_data["date1"]}
    if date_str["date"] == "":
        return redirect("/error")
    date = pd.to_datetime(date_str["date"]).date()
    fname = runmodel(date)
    return redirect(url_for("output", file=fname))


def search():
    return make_response(
        render_template("index.html", title="Mosquito Know", today=today_str(), oneweek=one_week())
    )
