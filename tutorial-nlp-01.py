from urllib import request
from nltk import word_tokenize
import nltk


"""
Descarga de un texto
"""
url = "http://www.gutenberg.org/cache/epub/41575/pg41575.txt"
response = request.urlopen(url)
raw = response.read().decode('utf8')

print(type(raw))
print(len(raw))
print(raw[:75])

"""­
Tokenización del texto
"""
tokens = word_tokenize(raw)
print(type(tokens))
print(len(tokens))
print(tokens[:10])

text = nltk.Text(tokens)
type(text)


