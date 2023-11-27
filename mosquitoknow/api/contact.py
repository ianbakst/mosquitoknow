from flask import make_response, render_template


def search():
    return make_response(render_template("contact.html", title="Mosquito Know"))
