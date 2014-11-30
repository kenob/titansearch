from flask.ext.script import Manager
from app import application, wiki, news, keyword_extractor, logger
import os
from urllib import *
import json, time, requests
from app.resources import api
from WikiExtractor import parse_wiki
from app.utils import get_top_terms, get_keywords
import time
import html5lib
from lxml import html

manager = Manager(application)

@manager.command
def runserver():
	from app import views
	api.init_app(application)
	application.run(debug = True)

@manager.command
def refresh_index(instance):
	"""
	Performs a full dataimport on either wikiArticleCollection or the newsArticleCollection
	params:
	instance: 'wiki' or 'news'
	"""
	base_url = application.config.get('SOLR_URI') + news

	if instance=='wiki':
		base_url = application.config.get('SOLR_URI') + wiki

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
				print "... processing %s documents" % stat			
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
def parse_wikimedia(input_dir = "E:/wikicorpus", 
					output_dir= "E:/wikicorpusclean"):
	"""
	Parses and generates keywords from Wikimedia articles
	params:
	input_dir: An absolute, flat directory containing ONLY wikimedia articles
	output_dir: The directory from which wikimedia articles are read by the wikiArticleCollection core
	""" 
	get_keywords = False
	if application.config.get('INDEX_KEYWORD_GENERATION'):
		get_keywords = True
	parse_wiki(input_dir, output_dir, 1024*1024, get_keywords)

@manager.command
def get_wiki_articles(output_dir):
	"""
	Collects keywords and topics from our news corpus and gets corresponding wikipedia pages
	params:
	output_dir: an empty/non-existent  sub-directory where the articles should be stored
	"""
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	q = get_top_terms("newsArticleCollection", "title", 100)
	if q['status'] == 'Unsuccessful':
		print "Solr request Unsuccessful"
		return
	words = q.get('words')
	logger.info(words)
	s = requests.Session()
	url = "http://en.wikipedia.org/w/index.php?title=Special:Export"
	pages = []
	for word in words:
		r = s.post(url, data=dict(action="submit",catname=word, addcat=True))
		doc = html5lib.parse(r.text)
		tree = html.fromstring(r.text)
		line = [td.text for td in tree.xpath("//*[@id='mw-content-text']/form/textarea")]
		pages_obtained = []
		for l in line:
			if l:
				pages_obtained = l.splitlines()
				pages += pages_obtained
		logger.info("%s page titles obtained for %s" % (len(pages_obtained), word))
	page_params = ("%0A").join(pages)
	logger.info("A total of %s page titles obtained, now getting pages from Wikipedia..." % len(pages))
	from_ = "2000-01-27T20:25:56Z"
	url = "http://en.wikipedia.org/w/index.php?title=Special:Export&pages=%s&offset=%s&limit=10000&action=submit"
	url = "http://en.wikipedia.org/wiki/Special:Export/"
	for i, page in enumerate(pages):
		r = s.get(url+page)
		with open(os.path.join(output_dir, "wiki_%s.xml" % i), 'wr') as out:
			out.write(r.text.encode('utf8'))

@manager.command
def test_kwextractor():
	res = keyword_extractor.extract_keywords()
	if res['status']:
		for k in res['keywords']:
			print k
	else:
		print "There was a connection problem"

@manager.command
def test_topic_extractor():
	sentence = """T Frustrated at the lack of a good screening test for ovarian cancer, advocacy groups have persuaded professional cancer 
		 organizations to endorse a list of persistent symptoms that might indicate the presence of the disease. The list could have a very beneficial 
		 effect in alerting patients -- and doctors who have been dismissive of complaints of generalized discomfort -- that ovarian cancer is present
		 at an early stage when it is most treatable.","Among the flood of patients who have the all-too-common symptoms, there will be some who 
		 undergo needless surgeries to remove ovaries that turn out not to be cancerous. That is the price that may be paid for this modest step 
		 toward detecting a cancer that typically kills 
	     most women who have it."""
	print get_keywords(sentence)

if __name__=="__main__":
	manager.run()