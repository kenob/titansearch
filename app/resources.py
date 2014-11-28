from flask.ext import restful
from flask import request, make_response
from utils import search, get_item, parse_to_alphanumeric
from .keyword_extractor import extract_keywords
from app import application, news, wiki
from flask.ext.restful import reqparse
from json import dumps


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

		search_results = search(wiki, query_term, page=page, rows=rows)

		error_message = "No results found for your search!"

		if search_results:
			if len(search_results)>1:
				error_message = ""
				for res in search_results:
					res['wiki_body'] = parse_to_alphanumeric(res['wiki_body'][0])
		return dict(search_results=search_results, error_message=error_message, query_term=qt, current_page=page), 200
	def post(self,**kwargs):
		return


class SearchResult(restful.Resource):
	def get(self,**kwargs):
		result_id = kwargs.get('wiki_id')
		related_news = []
		related_tweets = []
		wiki_article = dict()
		news_articles = []

		wiki_article_solr = get_item(wiki, result_id)
		if wiki_article_solr:
			wiki_article = wiki_article_solr

		tx = parse_to_alphanumeric(wiki_article.get('wiki_body',['hello world'])[0])

		keywords = extract_keywords(tx).get('keywords')		
		query_terms = []

		#TODO: Summarize wikipedia articles for display

		#since we are favoring precision over recall
		if len(keywords) > 1:
			for t in keywords:
				query_terms += t.split()
			query_term = "+".join(query_terms)
			news_articles = search(news, query_term)

		if news_articles:
			#TODO: remove the list comprehension, it was just for design purposes
			related_news = [news_article for news_article in news_articles if news_article.get('news_body')]

		return dict(related_news=related_news, wiki_article=wiki_article, related_tweets=related_tweets)
	def post(self, **kwargs):
		return

api.add_resource(Search, '/api/async/v1/')
api.add_resource(SearchResult, '/api/async/v1/results/<wiki_id>')