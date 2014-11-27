from flask.ext.script import Manager
from app import application
import os
from urllib import *
import json
import time
import requests
from app import keyword_extractor

manager = Manager(application)

@manager.command
def runserver():
	from app import views
	application.run(debug = True)

@manager.command
def refresh_index(corpus_type="NYC"):
	base_url = application.config.get('SOLR_NEWSCOLLECTION')
	try:
		r = requests.get('%s/dataimport?command=full-import' % base_url)
		print "Started indexing"
	except:
		print "Import could not be started. Please make sure the newsArticleCollection instance is configured properly and running"
		return
	retries = 0
	while True:
		try:
			status_conn = urlopen('%s/dataimport?command=status&wt=python' % base_url)
			status_response = eval(status_conn.read())
			stat = status_response["statusMessages"].get("Total Documents Processed",False)
			if stat:
				print "... %s documents processed" % stat			
			if status_response['status'] is 'idle':
				print "\n", status_response["statusMessages"][""]
				break
			time.sleep(5)
		except:
			retries = retries + 1
			if retries > 10:
				print "Cannot Get status, please check your solr server"
				break


@manager.command
def test_kwextractor():
	res = keyword_extractor.extract_keywords()
	if res['status']:
		for k in res['keywords']:
			print k
	else:
		print "There was a connection problem"



if __name__=="__main__":
	manager.run()