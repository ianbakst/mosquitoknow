#!/usr/local/bin/python
from flaskapp import app
app.config['TEMPLATES_AUTO_RELOAD']=True
app.run(debug = True,host= '0.0.0.0')
