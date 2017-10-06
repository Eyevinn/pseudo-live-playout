from flask import Flask
from redis import Redis, RedisError
import os
import socket
import sys
import cgi
from flask import request

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

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

@app.route("/ver", methods=['GET', 'POST'])
def ver():
	return "<h3>--- Version 5 ---</h3>"

@app.route("/test", methods=['GET', 'POST'])
def test():

	id = '';
	if request.method == 'POST':
		if 'id' in request.form:
			id = request.form['id']
	if request.method == 'GET':
		id = request.args.get('id', '')

	html = "<h3>Test</h3>" \
	       "<b>Id: </b> {id}<br>"

	return html.format(id=id)


@app.route("/log", methods=['GET', 'POST'])
def log():

	id = '';
	if request.method == 'POST':
		if 'id' in request.form:
			id = request.form['id']
	if request.method == 'GET':
		id = request.args.get('id', '')

	html = "<h3>hi {name}!</h3>" \
	       "<b>Id: </b> {id}<br>" \
	       "<b>Hostname:</b> {hostname}<br/>"

	return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), id=id)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

