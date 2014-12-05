import os
import sys
import os
from nltk.corpus import stopwords
from app import logger

stop = stopwords.words('english')

def clean(text):
	return ' '.join([''.join(e) for e in text.split() if e.isalnum()]).strip()

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
				with open(os.path.join(category_path, article)) as contents:
					text = ""
					for content in contents:
						if not content.isspace():
							if title:
								header = '<head>\n'
								print >> fileout, '<title>' + clean(content) + '</title>\n'
								title = False
								print >> fileout, header
								print >> fileout, '<docdata>'
	  							print >> fileout, '<doc-id id-string="%s"/>' % (10000000 + index)
	  							keys = [i for i in clean(content).lower().split() if i not in stop]
								print >> fileout, '<identified-content>\n'
		  					elif author:
								author = False
								if '<AUTHOR>' in content:
									content = content.replace('<AUTHOR>','').replace('</AUTHOR>','')
								print >> fileout, '<classifier>' + clean(content) + '</classifier>\n'
								print >> fileout, keyhead				
								print >> fileout, (" ").join(keys + [cat])
								print >> fileout, keyfooter
								print >> fileout, '</identified-content>\n'
								print >> fileout, '</docdata>\n'
								print >> fileout, '</head>\n'
								print >> fileout, bodyhead
							else:
								text += content
					print >> fileout, clean(text)
					print >> fileout, bodyfooter
					print >> fileout, footer
		print >> fileout, "</mediawiki>"
			
			