from flask import make_response, render_template, redirect, request


def search():
    file = request.args.get("file")
    return make_response(render_template("output.html", title="Mosquito Know", file=file))


def post():
    return redirect("/index")
