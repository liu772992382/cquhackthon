#!/usr/bin/env python
class Config(object):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:19951028liu@localhost:3306/hackthon?charset=utf8'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = 'cquhackthon'
