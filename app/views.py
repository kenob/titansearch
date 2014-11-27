from app import application, news, wiki
from flask import render_template, request, url_for, redirect
from .forms import SearchForm
from utils import search, get_item, parse_to_alphanumeric
from .keyword_extractor import extract_keywords
from .search_twitter import search_twitter


#TODO: We might need to seperate the search page from the home page, having a post method on '/' doesn't seem right
@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm();
	if form.validate_on_submit():
		return redirect(url_for('results', q=form.query.data))
	return render_template('index.html', form = form);

@application.route('/results', methods=['GET', 'POST'])
def results():
	qt = request.args.get('q')
	query_terms = qt.split()
	query_term = "+".join(query_terms)
	search_results = search(wiki, query_term, hl="true")

	error_message = "No results found for your search!"

	if search_results:
		if len(search_results)>1:
			error_message = ""
			for res in search_results:
				res['wiki_body'] = parse_to_alphanumeric(res['wiki_body'][0])

	return render_template('results.html', **locals());

@application.route('/related/<result_id>')
def related(result_id):
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
	twitter_query = "";
	#TODO: Summarize wikipedia articles for display

	#since we are favoring precision over recall
	if len(keywords) > 1:
		for t in keywords:
			query_terms += t.split()
		query_term = "+".join(query_terms)
		twitter_query = " OR ".join(query_terms)

		news_articles = search(news, query_term)
	statuses = search_twitter(twitter_query) ;
	
	if news_articles:
		#TODO: remove the list comprehension, it was just for design purposes
		related_news = [news_article for news_article in news_articles if news_article.get('news_body')]

	return render_template('related.html',**locals());
