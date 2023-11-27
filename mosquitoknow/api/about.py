from flask import make_response, render_template


def search():
    return make_response(render_template("about.html", title="Mosquito Know"))
