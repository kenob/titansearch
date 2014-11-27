from app import application
from urllib import *

base_url = application.config.get('SOLR_URI')

def search(collection, query_string="*:*", **kwargs):
	additional_args = ('&').join(["%s=%s" % (key,kwargs[key]) for key in kwargs])
	try:
		conn = urlopen('%s%s/select/?&q=%s&wt=python&%s' % (base_url, collection, query_string, additional_args))
		result = eval(conn.read())
		return result['response']['docs']
	except:
		return False


def get_item(collection, _id, **kwargs):
	additional_args = ('&').join(["%s=%s" % (key,kwargs[key]) for key in kwargs])
	try:
		conn = urlopen('%s%s/get/?&id=%s&wt=python&%s' % (base_url, collection, _id, additional_args))
		result = eval(conn.read())
		return result['doc']
	except:
		return False