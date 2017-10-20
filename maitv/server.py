from flask import Flask
from redis import Redis, RedisError
import os
import socket
import sys
import cgi
import time
from flask import request
from vodtolive import HLSVod
from User import User

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

starttime = time.gmtime()

usermap = {}

@app.route("/")
def hello():
	try:
		visits = redis.incr("counter")
	except RedisError:
		visits = "<i>cannot connect to Redis, counter disabled</i>"

	html = "<h3>Hello {name}!</h3>" \
	       "<b>Hostname:</b> {hostname}<br/>" \
	       "<b>Visits:</b> {visits}"
	return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

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
	html = "all ok, user id : {uid}"
	return html.format(uid=uid)

@app.route("/start", methods=['GET', 'POST'])
def start():
	if request.method == 'POST':
		if 'uid' in request.form:
			uid = request.form['uid']
	if request.method == 'GET':
		uid = request.args.get('uid', '')
	print len(usermap)
	for key in usermap:
		print("KEY:")
		print key
	u = usermap[uid]
	html = "Hello there "
	html += u.get_name
	html += " \n"

@app.route("/play.m3u8", methods=['GET', 'POST'])
def play():
	
	vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')
	mastermanifeststring = vod.get_live_master_manifest()
	return mastermanifeststring





@app.route("/pause", methods=['GET', 'POST'])
def pause():
	# later
	return "ok"



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)

