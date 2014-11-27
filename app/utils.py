from app import application, logger
from urllib import *
import re
from .wiki_extractor import clean

base_url = application.config.get('SOLR_URI')

def search(collection, query_string="*:*", page=1, rows=10, **kwargs):
	start = ((page-1) * rows)
	kwargs.update(dict(start=start, rows=rows))

	kwargs["hl.fragsize"] = application.config.get('SNIPPET_FRAGMENT_SIZE')
	kwargs["hl.snippets"] = application.config.get('SNIPPET_MAX')
	kwargs["hl"] = application.config.get('SNIPPET_GENERATION')
	kwargs["hl.simple.pre"] = application.config.get('SNIPPET_OPENING')
	kwargs["hl.simple.post"] = application.config.get('SNIPPET_CLOSING')
	kwargs["hl.fl"] = application.config.get('SNIPPET_FIELDS')

	additional_args = ('&').join(["%s=%s" % (key,kwargs[key]) for key in kwargs])
	try:
		conn = urlopen('%s%s/select/?&q=%s&wt=python&%s' % (base_url, collection, query_string, additional_args))
		result = eval(conn.read())
		return result['response'].get('docs',[]), result.get('highlighting',dict())
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

def parse_to_alphanumeric(input_string):   
   pattern = re.compile('[\W_]+')
   ret = pattern.sub(" ", input_string)
   return ret

def clean_wiki(w_list):
	logger.info("entry: %s" % w_list)
	page=[]
	res = "...".join(w_list)
	res = clean(res)
	p = re.compile("[\[[\]]\|\=]")
	p.sub(" ", res)
	return res

