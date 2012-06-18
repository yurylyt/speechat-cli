#!/usr/bin/python
import httplib
import json
import re
from sys import argv

def auth_token():
	return open('auth_token', 'r').read()

def call_speechat_auth(method, url):
	return call_speechat(method, url, {"auth-token": auth_token()})
def call_speechat(method, url, headers={}):
	conn = httplib.HTTPConnection("speechat.co")
	url = "/rest/" + url
	conn.request(method, url, "", headers)
	response = conn.getresponse()
	if (response.status > 299):
		raise Exception("Failed to do %s to %s. Status code: %d" % (method, url, response.status))
	return response.read()

def qs(chat_room):
	url = "chat/%s/p" % chat_room
	raw_data = call_speechat("GET", url)
	data = json.loads(raw_data)
	msgs = data['messages']

	for msg in msgs:
		print_if_q(msg)

def print_if_q(msg):
	if (re.match(".+\?.*", msg['message'])):
		print_msg(msg)

def print_msg(msg):
	print "%s: %s" %(msg['author'], msg['message'])

def users(room):
	print call_speechat_auth("GET", "admin/%s/users" % room)

def create(room):
	print "creating room %s " % room
	call_speechat_auth("POST", "admin/%s" % room)

if __name__ == "__main__":
	script, room, action = argv
	locals()[action](room)