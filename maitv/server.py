from flask import Flask
from redis import Redis, RedisError
import os
import socket
import sys
import cgi
import time
from flask import request
from vodtolive import HLSVod

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

starttime = gmtime()

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

@app.route("/start", methods=['GET', 'POST'])
def start():
	starttime = gmtime()
	return "ok"

@app.route("/pause", methods=['GET', 'POST'])
def pause():
	# later
	return "ok"

#		id = '';
#	if request.method == 'POST':
#		if 'id' in request.form:
#			id = request.form['id']
#	if request.method == 'GET':
#		id = request.args.get('id', '')



@app.route("/play.m3u8", methods=['GET', 'POST'])
def play():
	
	vod = HLSVod('http://dw2nch8cl472k.cloudfront.net/HLS/Apple%20HLS/HTTP%20example.m3u8')

	mastermanifeststring = vod.get_live_master_manifest()

	return mastermanifeststring



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

