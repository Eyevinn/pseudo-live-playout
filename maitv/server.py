from flask import Flask
from redis import Redis, RedisError
import os
import socket
import sys
import cgi
import time
from flask import request
from flask import Response
from vodtolive import HLSVod
from User import User
from flask_cors import CORS

from flask import Flask, request, send_from_directory
from flask import render_template


#from flask.ext.cors import CORS, cross_origin

#cors = CORS(app, resources={r"/foo": {"origins": "*"}})

# set the project root directory as the static folder, you can set others.
#app = Flask(__name__, static_url_path='/views')
#
#@app.route('/views')
#def send_js(path):
#    return send_from_directory('views', index.html)

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

starttime = time.gmtime()

usermap = {}

#@app.route("/")
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	'''try:
		visits = redis.incr("counter")
	except RedisError:
		visits = "<i>cannot connect to Redis, counter disabled</i>"

	html = "<h3>Hello {name}!</h3>" \
	       "<b>Hostname:</b> {hostname}<br/>" \
	       "<b>Visits:</b> {visits}"
	return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
	#return render_template('index.html')'''
	#return render_template('index.html')
	return render_template('index.html', name=name)

@app.route("/css/style.css", methods=['GET', 'POST'])
def css():
	print "serving css"
	#return render_template('data.json'), 201, {'Content-Type': 'application/json'}
	return render_template('css/style.css'), 200, {'Content-Type': 'text/css'}

@app.route("/js/index.js", methods=['GET', 'POST'])
def js():
	return render_template('js/index.js'), 200, {'Content-Type': 'text/js'}


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if 'user' in request.form:
			user = request.form['user']
	if request.method == 'GET':
		user = request.args.get('user', '')
	u = User(user)
	uid = u.my_id
	usermap[uid] = u
	print len(usermap)
	html = "{uid}"
	return html.format(uid=uid)
	#return render_template('index.html', user=u.get_name)

@app.route("/start", methods=['GET', 'POST'])
def start():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	#print len(usermap)
	#for key in usermap:
	#	print("KEY:")
	#	print key
	#print uid
	u = usermap[ int(uid) ]
	html = "Hello there {name} \n"
	#return html.format( name=u.get_name() )
	return render_template('index.html', user=u.get_name())

MIMETPE = 'application/x-mpegURL'
#MIMETPE = 'text/m3u8'

@app.route("/view.html", methods=['GET', 'POST'])
def view():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	
	u = usermap[ int(uid) ]

	res = "" + u.request_main(uid)

	return render_template('playlistview.html', res=res), 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, HEAD', 'Access-Control-Max-Age': 3000}

#('Access-Control-Allow-Origin', '*')
#	return render_template('js/index.js'), 200, {'Content-Type': 'text/js'}

@app.route("/play.m3u8", methods=['GET', 'POST'])
def play():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')

	print "got uid " + str(uid)
	
	u = usermap[ int(uid) ]

	print "usermap lookup ok"

	res = "" + u.request_main(uid)

	print "have result request main : " + res

	#vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
	#mastermanifeststring = vod.get_live_master_manifest()
	#mastermanifeststring = vod.get_user_master_manifest(uid)

	return Response(res,mimetype=MIMETPE)

@app.route("/variant.m3u8", methods=['GET', 'POST'])
def variant():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
		if 'btr' in request.form:
			btr = request.form['uid']

	if request.method == 'GET':
		uid = request.args.get('uid', '')
		btr = request.args.get('btr', '')

	#print "--- VARIANT ---"
	#print uid
	#print btr

	u = usermap[ int(uid) ]

	#print "got user " + u.get_name()

	variant = u.request_variant(btr)
	u.next()

	return Response(variant,mimetype=MIMETPE)


@app.route("/pause", methods=['GET', 'POST'])
def pause():
	# later
	return "ok"



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)

