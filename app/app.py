from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bucketlist.db"
app.config["SECRET_KEY"] = "kinggaamuwasamuel"

db = SQLAlchemy(app)