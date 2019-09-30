from flask import Flask
app = Flask(__name__)
from flaskapp import views
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
