from flask import Flask
app.config['TEMPLATES_AUTO_RELOAD'] = True
app = Flask(__name__)
from flaskapp import views
