from flask import Flask, render_template, redirect
from flask import request, url_for

from . import index


def get():
    print("HELLO!!!")
    return redirect("/index")
