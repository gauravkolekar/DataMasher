from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from logging.handlers import RotatingFileHandler
import os
import logging

app = Flask(__name__)
app.config.from_object(Config)
mongodb = PyMongo(app)

from application import routes

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/datamasher.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('DataMasher startup')
