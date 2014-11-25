from flask.ext.script import Manager
from app import application
import os
from urllib import *
import json
import time
import requests

manager = Manager(application)

@manager.command
def runserver():
	application.run(debug = True)

@manager.command
def refresh_index(corpus_type="NYC"):
	base_url = application.config.get('SOLR_NEWSCOLLECTION')
	r = requests.get('%s/dataimport?command=full-import' % base_url)
	while True:
		status_conn = urlopen('%s/dataimport?command=status&wt=python' % base_url)
		status_response = eval(status_conn.read())
		if status_response['status'] is 'idle':
			print status_response["statusMessages"][""]
			break
		time.sleep(10)
		print "still working..."


if __name__=="__main__":
	manager.run()