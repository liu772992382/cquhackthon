#!/usr/bin/env python
#coding=utf-8
import hashlib
from M2Crypto import util
from Crypto.Cipher import AES
from flask import Flask, request, render_template,redirect,make_response,flash,session,g,url_for,jsonify
import json
app = Flask(__name__)

def decrypt(data):
	iv = '9b738aa2ee18145a' # app id
	KEY = '298fe57f669647ffe92ee1deba8b944e' # app secret
	mode = AES.MODE_CBC
	data = util.h2b(data)
	decryptor = AES.new(KEY, mode, IV=iv)
	plain = decryptor.decrypt(data)
	print plain
	plain = "".join([ plain.strip().rsplit("}" , 1)[0] ,  "}"] )
	oauth_state = json.loads(plain)
	return oauth_state


def hashpw(a):
	ha=hashlib.md5()
	ha.update(a)
	print str(ha.hexdigest()),a
	return str(ha.hexdigest())


@app.route('/yiban',methods = ['GET'])
def yiban():
	x=request.args['test']
	print x
	return '31531'
	# info=decrypt(x[1])
	# print info
	# return info

@app.route('/',methods = ['GET'])
def index():
	return 'success'

if __name__=='__main__':
	app.run(host='0.0.0.0',port=2222, debug=True)
