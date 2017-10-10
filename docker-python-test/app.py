
from flask import Flask
from redis import Redis, RedisError
from flask import request

import os
import socket
import sys
import cgi
#import socket
import json



# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


@app.route("/")
def hello():

	html = "<h3> PCE ver 0.1.06 </h3>" \
	       "This service is not intended to be used manually <br/>" \
	       "Please use the associated client <br/>"
	return html.format()


sessions =  {                                           \
	2001 : {                                          \
		'sid' : 2001,                                   \
		'pid' : 1001,                                   \
		'name' : 'default',                             \
		'tabl' : ['prg001', 'prg002', 'prg003']         \
	},                                                  \
	2002 : {                                          \
		'sid' : 2002,                                   \
		'pid' : 1002,                                   \
		'name' : 'daniel',                              \
		'tabl' : ['prg004', 'prg003', 'prg002']         \
	},                                                  \
}




@app.route("/login", methods=['GET', 'POST'])
def login():

	name = '';
	if request.method == 'POST':
		if 'name' in request.form:
			name = request.form['id']
	if request.method == 'GET':
		name = request.args.get('name', '')

	pid = 1001
	sid = 2001
	if name == 'daniel':
		pid = 1002
		sid = 2002

	html = "Login successful<br>" \
	       "pid:{pid}<br>" \
	       "sid:{sid}<br>"

	return html.format(pid=pid, sid=sid)


@app.route("/playlist.m3u8", methods=['GET', 'POST'])
def playlist():

	sid = '';
	if request.method == 'POST':
		if 'sid' in request.form:
			sid = request.form['sid']
	if request.method == 'GET':
		sid = request.args.get('sid', '')

	post = {}

	if sid in sessions:
		post = sessions[sid]
	else:
		return ''

	segment = ''

	for item in post['tabl']:

		segment += seglist(item)

	return segment


@app.route("/tableau", methods=['GET', 'POST'])
def tableau():

	sid = '';
	if request.method == 'POST':
		if 'sid' in request.form:
			sid = request.form['sid']
	if request.method == 'GET':
		sid = request.args.get('sid', '')

	if sid in sessions:

		post = sessions[sid]

		html = "<h3>Program tableau for {name}<h3><br>";

		for t in post['tabl']:
			html += t + '<br>'

		return html.format(name=post['name'])

	else:

		html = "Error 404 no such session id ({sid})<br>";
		return html.format(sid=sid)


@app.route("/debug", methods=['GET', 'POST'])
def debug():

	html = ''
	for key1 in sessions:
		val1 = sessions[key1]
		html += "<h2>" + str(key1) + "</h2>"
		for key2 in val1:
			val2 = val1[key2]
			html += str(key2) + " : " +str(val2) + " <br>"
	html += "<br><br>\n"
	html += "<pre>\n"
	html += json.dumps(sessions, skipkeys=False, sort_keys=True, indent=4, separators=(', ', ' : '))
	html += "</pre>\n"

	return html


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

