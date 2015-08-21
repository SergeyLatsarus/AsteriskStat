# -*- coding: utf-8 -*-
from flask import Flask
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
from app import views
app.config.from_object('config')
