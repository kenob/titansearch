from flask import Flask;
from logging import StreamHandler, Formatter
import logging
import HTMLParser

application = Flask(__name__);
application.config.from_object('config')

news = application.config.get('NEWS_COLLECTION_INSTANCE')
wiki = application.config.get('WIKI_ARTICLE_INSTANCE')

file_handler = StreamHandler()
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
application.logger.setLevel(logging.INFO) 
application.logger.addHandler(file_handler)
logger = application.logger

html_parser = HTMLParser.HTMLParser()
