from app import application, news, wiki, logger
from flask import render_template, request, url_for, redirect
from .forms import SearchForm
from utils import search, get_item, parse_to_alphanumeric, clean_wiki
from .keyword_extractor import extract_keywords
from .wiki_extractor import clean
from .search_twitter import search_twitter
import urllib
import json

initial_query = "";
#TODO: We might need to seperate the search page from the home page, having a post method on '/' doesn't seem right
@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm();
	initial_query = form.query.data;
	if form.validate_on_submit():
		return redirect(url_for('results', q=form.query.data))
	return render_template('index.html', form = form);

@application.route('/results', methods=['GET', 'POST'])
def results():
	qt = request.args.get('q')
	query_terms = qt.split()
	query_term = "+".join(query_terms)
	form = SearchForm();

	sear = search(wiki, query_term, hl="true")
	error_message = "No results found for your search!"

	# for Did you mean? section
	# http://localhost:8983/solr/wikiArticleCollection/spell?q=alternatie&wt=json&indent=true
	params = urllib.urlencode({'q': initial_query, 'wt': "json", 'indent' : "true" })
	try:
		did_you_mean_json = urllib.urlopen("http://localhost:8983/solr/wikiArticleCollection/spell?%s" % params)
	except:
		response = None;



	#currently returning only results that were highlighted
	if sear:
		search_results = sear[0]
		result_snippets = sear [1]
		for res in search_results:
			_id = res['id']
			if _id in result_snippets:
				try:
					res['wiki_body'] = ("...").join(result_snippets[_id].get('wiki_body', []))
				except:
					del search_results[_id]
			else:
				del search_results[_id]

		if search_results:
			if len(search_results)>0:
				error_message = ""

	return render_template('results.html', **locals());

@application.route('/related/<result_id>')
def related(result_id):
	related_news = []
	related_tweets = []
	wiki_article = dict()
	news_articles = []
	form = SearchForm();


	wiki_article_solr = get_item(wiki, result_id)
	if wiki_article_solr:
		wiki_article = wiki_article_solr

	query_terms = []

	twitter_query = "";

	keywords = wiki_article.get('keywords',[])

	if not application.config.get('INDEX_KEYWORD_GENERATION'):
		keywords = extract_keywords(wiki_article['wiki_body'][0].encode('utf-8')).get('keywords')

	#since we are favoring precision over recall
	if len(keywords) > 1:
		for t in keywords:
			query_terms += t.split()
		query_term = "+".join(query_terms)
		twitter_query = " OR ".join(query_terms)

		news_articles = search(news, query_term)
	related_tweets = search_twitter(twitter_query) ;

	print twitter_query;
	if news_articles:
		news_articles = news_articles[0]
		#TODO: remove the list comprehension, it was just for design purposes
		related_news = [news_article for news_article in news_articles if news_article.get('news_body')]

	return render_template('related.html',**locals());

@application.route('/async')
def index_async():
	return render_template('index_async.html');