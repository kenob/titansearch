from app import application, logger
from urllib import *
import re
from .wiki_extractor import clean
# from nltk.corpus import stopwords
# from nltk.tag.stanford import NERTagger

# stop = stopwords.words('english')
# st = NERTagger('/home/kenob/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
#                 '/home/kenob/stanford-ner-2014-06-16/stanford-ner.jar')

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
		numRes = result['response'].get('numFound')
		results_left = int(numRes) - (start + rows)
		num_pages = numRes/rows
		return result['response'].get('docs',[]), result.get('highlighting',dict()), results_left, numRes
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

def get_top_terms(collection="newsArticleCollection", field="keywords", limit=100):
	params = "terms.fl=%s&terms.lower=a&omitHeader=true&terms.limit=%s&wt=python" % (field, limit)
	base_url = application.config.get('SOLR_URI') + collection
	url = base_url + "/terms?" + params
	res = dict()
	try:
		conn = urlopen(url)
		res = eval(conn.read())
		logger.info(res)
	except:
		return dict(status="Unsuccessful", words=[])
	words = [r for r in res['terms'].get(field,[]) if not type(r)==int]
	logger.info(words)
	return dict(status="Successful", words=words)

def parse_to_alphanumeric(input_string):   
   pattern = re.compile('[\W_]+')
   ret = pattern.sub(" ", input_string)
   return ret

def clean_wiki(w_list):
	logger.info("entry: %s" % w_list)
	res = clean(w_list[0])
	return [res]

def get_keywords(text):
	# np_extractor = NPExtractor(text)
	# result = np_extractor.extract()
	# return result
	# s = st.tag(text.split())
 # 	i = list({j[0] for j in s if j[1]!=u'O'})
 # 	out = [ii for ii in i if ii.lower() not in stop]
 	return []
