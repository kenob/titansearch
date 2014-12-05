import os
import sys
import os
# from nltk.corpus import stopwords
# from nltk.tag.stanford import NERTagger
from app import logger
from app.utils import get_keywords

# stop = stopwords.words('english')
# st = NERTagger('/home/kenob/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
# 	'/home/kenob/stanford-ner-2014-06-16/stanford-ner.jar')


def clean(text):
	return ' '.join([''.join(e) for e in text.split() if e.isalnum()]).strip()
def clean_total(text):
	return ' '.join([''.join(e) for e in text.split() if e.isalpha()]).strip()

def parse_reuters(directory, output_dir):
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	with open(os.path.join(output_dir, 'reuters.xml'),'w') as fileout:
		index = 0
		bodyhead = "<body>\n <body.content>\n <block class='lead_paragraph'>\n"
		bodyfooter = "</block>\n </body.content>\n </body>"
		footer = "\n</nitf>"
		keyhead = "<classifier>"
		keyfooter = "</classifier>"
		categories = os.listdir(directory)
		print >> fileout, "<?xml version='1.0' encoding='UTF-8'?>\n" 
		print >> fileout, "<nitf>" 
		for cat in categories:
			category_path = os.path.join(directory, cat)
			articles = os.listdir(category_path)
			for article in articles:
				title = True
				author = True
				place = True
				index += 1
				keys = []
				titlestring = ""
				docdatastring = ""
				with open(os.path.join(category_path, article)) as contents:
					text = ""
					for content in contents:
						if not content.isspace():
							if title:
								header = '<head>\n'
								titlestring = '<title>' + clean(content) + '</title>\n'
								title = False
	  							docdatastring = '<doc-id id-string="%s"/>' % (10000000 + index)
	  							# keys = [i for i in clean_total(content).lower().split() if i not in stop]
		  					elif author:
								author = False
								if '<AUTHOR>' in content:
									content = content.replace('<AUTHOR>','').replace('</AUTHOR>','')
								text += clean(content)
							else:
								text += content
					cleaned_text = clean_total(text)
					keys = get_keywords(cleaned_text)
					print >>fileout, titlestring
					print >> fileout, header
					print >> fileout, '<docdata>'
					print >> fileout, docdatastring
					print >> fileout, '<identified-content>\n'
					print >> fileout, keyhead				
					print >> fileout, (" ").join(keys + [cat])
					print >> fileout, keyfooter
					print >> fileout, '</identified-content>\n'
					print >> fileout, '</docdata>\n'
					print >> fileout, '</head>\n'
					print >> fileout, bodyhead
					print >> fileout, clean(cleaned_text)
					print >> fileout, bodyfooter
					print >> fileout, footer
			
			