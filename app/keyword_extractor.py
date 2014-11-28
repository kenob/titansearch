
import urllib
import json

text = '''The Hubble Space Telescope (HST) is a space telescope that was launched into low Earth orbit in 1990 and remains in operation. With a 2.4-meter (7.9 ft) mirror, Hubble's four main instruments observe in the near ultraviolet, visible, and near infrared spectra. The telescope is named after the astronomer Edwin Hubble.

Hubble's orbit outside the distortion of Earth's atmosphere allows it to take extremely high-resolution images with almost no background light. Hubble has recorded some of the most detailed visible-light images ever, allowing a deep view into space and time. Many Hubble observations have led to breakthroughs in astrophysics, such as accurately determining the rate of expansion of the universe.

Although not the first space telescope, Hubble is one of the largest and most versatile, and is well known as both a vital research tool and a public relations boon for astronomy. The HST was built by the United States space agency NASA, with contributions from the European Space Agency, and is operated by the Space Telescope Science Institute. The HST is one of NASA's Great Observatories, along with the Compton Gamma Ray Observatory, the Chandra X-ray Observatory, and the Spitzer Space Telescope.[5]

Space telescopes were proposed as early as 1923. Hubble was funded in the 1970s, with a proposed launch in 1983, but the project was beset by technical delays, budget problems, and the Challenger disaster. When finally launched in 1990, Hubble's main mirror was found to have been ground incorrectly, compromising the telescope's capabilities. The optics were corrected to their intended quality by a servicing mission in 1993.

Hubble is the only telescope designed to be serviced in space by astronauts. After launch by Space Shuttle Discovery in 1990, four subsequent Space Shuttle missions repaired, upgraded, and replaced systems on the telescope. A fifth mission was canceled on safety grounds following the Columbia disaster. However, after spirited public discussion, NASA administrator Mike Griffin approved one final servicing mission, completed in 2009. The telescope is still operating as of 2014, and may last until 2020.[6] Its scientific successor, the James Webb Space Telescope (JWST), is scheduled for launch in 2018.'''


def extract_keywords(body_text):
	precision = 0.9;
	app_key = '9be64884189dc6bfb19e341ee93a48b7'
	app_id = 'af1ed7e7'
	params = urllib.urlencode({'lang': 'en', 'text': body_text, 'min_confidence' : precision,  'include' :'types,abstract,categories,lod','$app_id': app_id, '$app_key' : app_key   })
	data = dict()
	try:
		response = urllib.urlopen("https://api.dandelion.eu/datatxt/nex/v1/?%s" % params)
		data = json.load(response)
	except:
		return dict(status=False, keywords=[])

	if not 'annotations' in data:
		return dict(status=True, keywords=[])

	return dict(status=True, keywords=[datum['spot'] for datum in data['annotations']])
	

