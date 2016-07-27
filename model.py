#!/usr/bin/env python
#coding=utf8

from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from config import Config
import sys, os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer,primary_key = True)
    school_id = db.Column(db.String(256),unique = True)
    school_name = db.Column(db.String(256))
    api_url = db.Column(db.String(512),unique = True)
    provide_user_name = db.Column(db.String(64))
    privide_user_id = db.Column(db.String(64))
    class_time = db.Column(db.String(512))

class User(db.Model):
    __tablename__ = 'Users'

    uid = db.Column(db.Integer, primary_key = True)
    yb_id = db.Column(db.String(64),unique = True)
    stu_num = db.Column(db.String(64))
    pass_word = db.Column(db.String(128))
    school_id = db.Column(db.String(256))
    date_time = db.Column(db.DateTime)
