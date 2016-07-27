#!/usr/bin/env python
#coding=utf-8
import hashlib
from M2Crypto import util
from Crypto.Cipher import AES
from flask import Flask, request, render_template,redirect,make_response,flash,session,g,url_for,jsonify
import json
from model import *
import requests
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
	print str(ha.hexdigest()),a
	return str(ha.hexdigest())

# def buildjson(data):



@app.route('/yiban',methods = ['GET'])
def yiban():
	x=request.args['verify_request']
	info = decrypt(x)
	userdata = {}
	userdata['access_token'] = info['visit_oauth']['access_token']
	userdata['id'] = info['visit_user']['userid']
	userdata['username'] = info['visit_user']['username']
	a = requests.get('https://openapi.yiban.cn/user/other?access_token='+userdata['access_token']+'&yb_userid='+userdata['id'],verify=False)
	userdata['school'] = a.json()['info']['yb_schoolname']
	userdata['token'] = hashpw(userdata['id']+'hackthon')
	user = User()
	school = School()
	if db.session.query(School).filter_by(school_id = a.json()['info']['yb_schoolid']).first() == None:
		school.school_id = a.json()['info']['yb_schoolid']
		school.school_name = a.json()['info']['yb_schoolname']
		db.session.add(school)
		db.session.commit()
	user.yb_id = userdata['id']
	user.school_id = a.json()['info']['yb_schoolid']
	try:
		if db.session.query(User).filter_by(yb_id = userdata['id']).first().stu_num != None:
			userdata['is_bind'] = True
		else:
			userdata['is_bind'] = False
	except:
		userdata['is_bind'] = False
	if db.session.query(User).filter_by(yb_id = userdata['id']).first() == None:
		db.session.add(user)
		db.session.commit()
	if db.session.query(School).filter_by(school_id = a.json()['info']['yb_schoolid']).first() != None:
		if db.session.query(School).filter_by(school_id = a.json()['info']['yb_schoolid']).first().api_url !=None:
			userdata['school_api'] = True
	else:
		userdata['school_api'] = False
	user_json = json.dumps(userdata)
	return "<html><head></head><body><script>window.local_obj.showSource('"+user_json+"');</script></body></html>"


@app.route('/bind',methods = ['GET'])
def user_bind():
	get_args = request.args
	if get_args['token'] == hashpw(get_args['id']+'hackthon'):
		user = db.session.query(User).filter_by(yb_id = get_args['id']).first()
		user.stu_num = get_args['jwc_name']
		user.pass_word = get_args['jwc_pass']
		db.session.commit()
		return 'success'
	else:
		return 'error'

@app.route('/getdata',methods = ['GET','POST'])
def getdata():
	get_args = request.args
	if get_args['token'] == hashpw(get_args['id']+'hackthon'):
		user = db.session.query(User).filter_by(yb_id = get_args['id']).first()
		school = db.session.query(School).filter_by(school_id = user.school_id).first()
		a = requests.get('http://'+school.api_url+'?name='+user.stu_num+'&pass='+user.pass_word)
		return a.text
	else:
		return 'error'


@app.route('/',methods = ['GET'])
def index():
	schools = db.session.query(School).all()
	return render_template('Index.html',schools = schools)



@app.route('/submit',methods = ['GET','POST'])
def submit():
	if request.method == 'GET':
		return render_template('Submit.html')
	elif request.method == 'POST':
		dataform = request.form
		school = db.session.query(School).filter_by(school_name = dataform['school_name']).first()
		if school == None or school.api_url == None:
			school.api_url = dataform['api_url']
			school.school_name = dataform['school_name']
			school.provide_user_name = dataform['provide_user_name']
			db.session.commit()
			return 'success'
		else:
			return 'error'
if __name__=='__main__':
	app.run(host='0.0.0.0',port=2222, debug=True)
