from app import application;
from flask import render_template;
from .forms import SearchForm;

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
	related_news = [{'id':'001','title':'Java jobs are in high demand','snippet':'Java developers in .....', 'url':'http://www.washingtonpost.com/what-developers-will-be-doing-learning-and-listening-to-in-2012-survey-results/2012/01/11/gIQA8VuxqP_story.html'},
					{'id':'002','title':'Python jobs are in high demand','snippet':'Python developers in .....', 'url':'http://www.washingtonpost.com/local/education/u-va-president-suspends-fraternities-until-jan-9-in-wake-of-rape-allegations/2014/11/22/023d3688-7272-11e4-8808-afaa1e3a33ef_story.html?tid=trending_strip_5'}]
	return render_template('related.html',related_news = related_news);