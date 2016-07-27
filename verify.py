#!/usr/bin/env python
#coding=utf-8
import hashlib
from M2Crypto import util
from Crypto.Cipher import AES
from flask import Flask, request, render_template,redirect,make_response,flash,session,g,url_for,jsonify
import json
app = Flask(__name__)

def decrypt(data):
	iv = '6baadc29cf37062a' # app id
	KEY = '9acfba94ad8877ed858e9acf01fe3acb' # app secret
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
	# print str(ha.hexdigest()),a
	return str(ha.hexdigest())

# def buildjson(data):



@app.route('/yiban',methods = ['GET'])
def yiban():
	x=request.args['verify_request']
	info = decrypt(x)
	print info
	info_json = json.dumps(info)
	return info_json


@app.route('/',methods = ['GET'])
def index():
	if request.method == 'GET':
		return render_template('Submit.html')
	elif request.method == 'POST':
		return 'success'

if __name__=='__main__':
	app.run(host='0.0.0.0',port=2222, debug=True)
