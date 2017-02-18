import os
from urllib import request
from nltk import word_tokenize
import nltk
from nltk import FreqDist
import pprint

"""
Descarga de un texto
"""

print("Descargando Juvenillia....")
if os.path.exists('juvenillia.txt'):
	with open('juvenillia.txt', "rt", encoding="utf-8") as f:
		raw = f.read()

else:
	url = "http://www.gutenberg.org/cache/epub/41575/pg41575.txt"
	response = request.urlopen(url)
	raw = response.read().decode('utf8')

	with open('juvenillia.txt', "wt", encoding="utf-8") as f:
		f.write(raw)

print("Tokenizando archivo....")
tokens = word_tokenize(raw)
text = nltk.Text(tokens)

def get_concordance_list(text, search, margin):

	c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
	return [text.tokens[offset-margin:offset+margin] for offset in c.offsets(search.lower())]



get_concordance_list(text, 'Nacional', 10)
# pprint.pprint(get_concordance_list(text, 'Nacional', 10))
text.collocations()

fdist1 = FreqDist(text)

fdist1.hapaxes()[:20]
