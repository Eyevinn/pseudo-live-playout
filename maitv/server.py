from flask import Flask
from redis import Redis, RedisError
import os
import socket
import sys
import cgi
import time
from random import seed
from flask import request
from flask import Response
from vodtolive import HLSVod
from User import User
from flask_cors import CORS

from flask import Flask, request, send_from_directory
from flask import render_template

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

starttime = time.gmtime()

usermap = {}

seed()

#@app.route("/")
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('index.html', name=name)

#Serve style.css
@app.route("/css/style.css", methods=['GET', 'POST'])
def css():
	return render_template('css/style.css'), 200, {'Content-Type': 'text/css'}

##Serve index.js
@app.route("/js/index.js", methods=['GET', 'POST'])
def js():
	return render_template('js/index.js'), 200, {'Content-Type': 'text/js'}

##Create a user, it will be assigned a user id
@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if 'user' in request.form:
			user = request.form['user']
	if request.method == 'GET':
		user = request.args.get('user', '')
		
	html = "{uid}"
		
	for uu in usermap:
		if usermap[uu].user_name == user:
			return html.format(uid=uid)
		
	u = User(user)
	uid = u.my_id
	usermap[uid] = u
	return html.format(uid=uid)


@app.route("/start", methods=['GET', 'POST'])
def start():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')

	u = usermap[ int(uid) ]
	html = "Hello there {name} \n"

	return render_template('index.html', user=u.get_name())

#Specifies mimetype
MIMETPE = 'application/x-mpegURL'

#Gets master playlist and video titles and returns it to "playlistview.html"
@app.route("/view.html", methods=['GET', 'POST'])
def view():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	
	if not (int(uid) in usermap):
		return "unknown uid<br>";

	u = usermap[ int(uid) ]
	
	u.restart()
	
	name = u.user_name

	res = "" + u.request_main(uid)

	jssnutt = " titles = ["
	first = True
	for t in u.titles:
		if not first:
			jssnutt += ", "
		jssnutt += '"' + str(t) + '"'
		first = False
	jssnutt += "];"

	return render_template('playlistview.html', name=name, uid=uid, res=res, jssnutt=jssnutt), 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, HEAD', 'Access-Control-Max-Age': 3000}


@app.route("/active", methods=['GET', 'POST'])
def active():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	
	html = ""
	if (uid):
		u = usermap[ int(uid) ]
		html += str(u.get_active())

	return html

#Gets master playlist
@app.route("/play.m3u8", methods=['GET', 'POST'])
def play():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	
	u = usermap[ int(uid) ]

	res = "" + u.request_main(uid)

	return Response(res,mimetype=MIMETPE)

#Gets variant playlists
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

	u = usermap[ int(uid) ]

	variant = u.request_variant(btr)
	u.next()

	return Response(variant,mimetype=MIMETPE)


@app.route("/pause", methods=['GET', 'POST'])
def pause():
	# later
	return "ok"


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)

