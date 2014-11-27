from app import application, news, wiki
from flask import render_template
from .forms import SearchForm
from utils import search, get_item

@application.route('/')
@application.route('/index')
def index():
	form = SearchForm();
	return render_template('index.html', form = form);

@application.route('/results', methods=['GET', 'POST'])
def results():
	search_results = [{'id':'001','title':'Java', 'snippet':'Java is a programming language', 'url':'http://en.wikipedia.org/wiki/Java_%28programming_language%29'},
					{'id':'002','title':'Microsoft', 'snippet':'Microsoft is a software company.', 'url':'http://en.wikipedia.org/wiki/Microsoft'}];
	return render_template('results.html', search_results = search_results);

@application.route('/related/<result_id>')
def related(result_id):
	related_news = []
	related_tweets = []
	wiki_article = dict(keywords=["Baseball", "Emmy"], 
						snippet='''Baseball (1994) is an 18 hour, 
									Emmy Award-winning documentary series by Ken 
									Burns about the game of baseball. First broadcast on PBS, 
									this was Burns' ninth documentary.
								''',
						title='Baseball documentary',
		 				id='001',
		 				url="http://en.wikipedia.org/wiki/Baseball_%28TV_series%29")

	#This will work properly only when the wiki article config has been set and the solr instance has been integrated properly
	#But as per the project specs, errors have already been handled in utils.py
	wiki_article_solr = get_item(wiki, result_id)
	if wiki_article_solr:
		wiki_article = wiki_article_solr
		
	query_terms = []

	for t in wiki_article.get('keywords',[]):
		query_terms += t.split()

	query_term = "+".join(query_terms)

	news_articles = search(news, query_term)

	if news_articles:
		#TODO: remove the list comprehension, it was just for design purposes
		related_news = [news_article for news_article in news_articles if news_article.get('news_body')]

	return render_template('related.html',**locals());
