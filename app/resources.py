from flask.ext import restful
from flask import request, make_response
from utils import search, get_item, get_top_terms, get_keywords, parse_to_alphanumeric
from .keyword_extractor import extract_keywords
from app import application, news, wiki, logger
from flask.ext.restful import reqparse
from json import dumps
from .search_twitter import search_twitter
from app import html_parser
import urllib
import json


api = restful.Api()
parser = reqparse.RequestParser()

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api.representations = DEFAULT_REPRESENTATIONS


class Search(restful.Resource):
	def get(self,**kwargs):
		parser.add_argument('q', type=str)
		parser.add_argument('page', type=int)
		parser.add_argument('rows', type=int)

		args = parser.parse_args()

		qt = args.get('q')
		if not qt:
			qt = '*:*'

		rows = args.get('rows')
		if not rows:
			rows = 10

		page = args.get('page')
		if not page:
			page = 1

		query_terms = qt.split()

		query_term = query_terms[0]

		if len(query_terms)>1:
			query_term = "+".join(query_terms)

		search_results = None
		search_results_ = search(wiki, query_term, page=page, rows=rows)
		num_pages = 0;

		error_message = "No results found for your search!"

		if search_results_:
			search_results = search_results_[0]
			result_snippets = search_results_[1]
			has_next = search_results_[2] > 1
			has_previous = (page - 1) > 0
			num_results = search_results_[3]
			
			for res in search_results:
				_id = res['id']
				if _id in result_snippets:
					try:
						res['wiki_body'] = ("...").join(result_snippets[_id].get('wiki_body', []))
					except:
						del search_results[_id]
				else:
					del search_results[_id]

		params = urllib.urlencode({'q': qt, 'wt': "json", 'indent' : "true" })
	
		did_you_mean = urllib.urlopen("http://localhost:8983/solr/wikiArticleCollection/spell?%s" % params)
		did_you_mean_object = json.load(did_you_mean)
		did_you_mean_words = [];
		try: 
			did_you_mean_words = [];
			for word in did_you_mean_object["spellcheck"]["suggestions"][1]["suggestion"]:
				did_you_mean_words.append(word["word"]);
		except: 
			did_you_mean_words = [];

			if search_results:
				if len(search_results)>0:
					error_message = ""
		suggested_terms = did_you_mean_words

		return dict(search_results=search_results, error_message=error_message, query_term=qt, 
					current_page=page, num_results=num_results, suggested_terms=suggested_terms), 200

	def post(self,**kwargs):
		return


class SearchResult(restful.Resource):
	def get(self,**kwargs):
		result_id = kwargs.get('wiki_id')
		related_news = []
		related_tweets = []
		wiki_article = dict()
		news_articles = []
		nearby = False;
		wiki_article_solr = get_item(wiki, result_id)
		if wiki_article_solr:
			wiki_article = wiki_article_solr

		query_terms = []

		twitter_query = "";

		keywords = wiki_article.get('keywords',[])

		#TODO: For large documents, get keywords for random parts of the document only, to keep the kw list short enough
		try:
			keywords = get_keywords(wiki_article['wiki_body'][0].decode())
		except:
			keywords = get_keywords(parse_to_alphanumeric(wiki_article['wiki_body'][0]))

		# if not application.config.get('INDEX_KEYWORD_GENERATION'):
		# 	keywords = extract_keywords(wiki_article['wiki_body'][0].encode('utf-8')).get('keywords')
		# 	logger.info(keywords)
		twitter_query = wiki_article["title"][0];

		#since we are favoring precision over recall
		query_terms = ["\""+t+"\"" for t in keywords]
		query_terms = wiki_article['title'][0].split()
		query_term = "+".join(query_terms)

		if query_term:
			news_articles = search(news, query_term, defType="edismax", mm=2, qf="title^20.0+keywords^20.0+body^2.0")[0]
		related_tweets = search_twitter(twitter_query, nearby) ;
		related_tweets = [html_parser.unescape(tweet) for tweet in related_tweets]
		return dict(related_news=news_articles[:3], wiki_article=wiki_article, related_tweets=related_tweets), 200
	def post(self, **kwargs):
		return

class Twitter(restful.Resource):
	def get(self, **kwargs):
		parser.add_argument('title', type=str)
		args = parser.parse_args()
		qt = args.get('q', "")
		tweets = search_twitter(qt, True);
		return dict(tweets=tweets), 200



api.add_resource(Search, '/api/async/v1/')
api.add_resource(SearchResult, '/api/async/v1/results/<wiki_id>')