from flask import Flask;

application = Flask(__name__);
application.config.from_object('config')

news = application.config.get('NEWS_COLLECTION_INSTANCE')
wiki = application.config.get('WIKI_ARTICLE_INSTANCE')
