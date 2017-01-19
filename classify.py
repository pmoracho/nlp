# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# parseit
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License
# as published by the Free Software Foundation. A copy of this license should
# be included in the file GPL-3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

__author__		= "Patricio Moracho <pmoracho@gmail.com>"
__appname__		= "classify"
__appdesc__		= "Clasificador de sentencias usando Clasificación Bayes ingenua"
__license__		= 'GPL v3'
__copyright__	= "2017, %s" % (__author__)
__version__		= "0.1"
__date__		= "2017/01/19"

"""
###############################################################################
# Imports
###############################################################################
"""
try:
	import sys
	import gettext

	def my_gettext(s):
		"""my_gettext: Traducir algunas cadenas de argparse."""
		current_dict = {
			'usage: ': 'uso: ',
			'optional arguments': 'argumentos opcionales',
			'show this help message and exit': 'mostrar esta ayuda y salir',
			'positional arguments': 'argumentos posicionales',
			'the following arguments are required: %s': 'los siguientes argumentos son requeridos: %s'
		}

		if s in current_dict:
			return current_dict[s]
		return s

	gettext.gettext = my_gettext

	# use natural language toolkit
	import nltk
	# from nltk.corpus import stopwords
	# from nltk.stem.lancaster import LancasterStemmer
	from nltk.stem import SnowballStemmer
	from nltk.corpus import stopwords
	import csv
	import pprint
	import pickle
	import argparse

except ImportError as err:
	modulename = err.args[0].split()[3]
	print("No fue posible importar el modulo: %s" % modulename)
	sys.exit(-1)


##################################################################################################################################################
# Inicializar parametros del programa
##################################################################################################################################################
def init_argparse():

	usage = '\nEjemplos de uso:\n\n' \
			'- Interpretar un archivo infiriendo el formato:\n' \
			'  %(prog)s [opciones] <archivo a interpretar>\n\n' \
			'- Mostrar todos los formatos disponibles y sus definiciones:\n' \
			'  %(prog)s [opciones] -s [opciones]\n\n' \
			'- Mostrar esta ayuda:\n' \
			'  %(prog)s -h\n\n'

	cmdparser = argparse.ArgumentParser(
							prog=__appname__,
							description="%s\n%s\n" % (__appdesc__, __copyright__),
							epilog=usage,
							formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=35),
							usage=None
	)

	cmdparser.add_argument('sentence', 			type=str, nargs='?', help="Sentencia a interpretar")

	cmdparser.add_argument("-v", "--version", 					action='version', version=__version__)
	cmdparser.add_argument('-t', '--train-file', 	type=str, 	action="store", dest="train_file", help="Definir el archivo de entrenamiento", metavar="\"path o archivo\"")
	"""
	cmdparser.add_argument('-a', '--addtotals', 				action="store_true", dest="addtotals", help="Agregar una última fila con los totales de los campos númericos")
	cmdparser.add_argument('-u', '--useformat', 	type=str, 	action="store", dest="useformat", help="Forzar el uso de un determinado formato para porcesar el archivo", metavar="\"formato\"")
	cmdparser.add_argument('-t', '--dontusetables', 			action="store_true", dest="dontusetables", help="No usar traducción por tablas y mostrar los datos nativos")
	cmdparser.add_argument('-s', '--showformat', 				action="store_true", dest="showformat", help="Mostrar información de un formato (--format) en particular o todos los definidos")
	cmdparser.add_argument('-i', '--ignorefmterror', 			action="store_true", dest="ignorefmterror", help="Ignorar errores al cargar archivos de formatos")
	cmdparser.add_argument('-o', '--outputfile', 				action="store", dest="outputfile", help="Exportar a un archivo", metavar="\"archivo\"")
	cmdparser.add_argument('-x', '--openfile', 					action="store_true", dest="openfile", help="abrir automáticamente el archivo")
	cmdparser.add_argument('-e', '--exportformat', 				action="store", dest="exportformat", help="Exportar en un formato específico", metavar="\"formato\"", default="psql")
	cmdparser.add_argument('-c', '--showcols', 		type=str, 	action="store", dest="showcols", help=u"Números de las columnas a mostrar", metavar="\"columnas\"")
	cmdparser.add_argument('-r', '--showrows', 		type=str, 	action="store", dest="showrows", help=u"Números de las filas a mostrar", metavar="\"filas\"")
	cmdparser.add_argument('-n', '--dontshowrecordnumber', 		action="store_false", dest="addrecordnumber", help="No mostrar los números de cada registro")
	cmdparser.add_argument('-z', '--horizontalmode', 			action="store_true", dest="horizontalmode", help="Modo de visualización horizontal")
	cmdparser.add_argument('-l', '--css-file', 					action="store", dest="cssfile", help="Archivo de estilos (.Css) para la salida Html", metavar="\"archivo css\"")
	cmdparser.add_argument('-b', '--search-text', 	type=str, 	action="store", dest="searchtext", help="Búsqueda y filtrado de texto", metavar="\"Texto a buscar\"")
	"""
	return cmdparser


def showerror(msg):
	print("\n!!!! %s error: %s\n" % (__appname__, msg))


class TextClasiffier(object):

	def __init__(self, languaje="spanish"):

		self.training_data  = []
		self.corpus_words   = {}
		self.tag_words      = {}
		self.languaje		= languaje

		self.stemmer = SnowballStemmer(self.languaje)

	def train_from(self, traindata_file):

		self.traindata_file = traindata_file
		self._read_training_data()

		# Armo la lista de tags a reconocer
		tags = list(set([a['tag'] for a in self.training_data]))
		for c in tags:
			self.tag_words[c] = []

		# print(len(self.tag_words))
		# print(len(self.training_data))

		# Proceso laq lista de entrenamiento
		for data in self.training_data:
			# Convierto cada sentencia en una lista de tokens quitando
			# stopwords y lematizando cada token
			for word in self.tokenize_and_stemm_sentence(data['sentence']):
				if word not in self.corpus_words:
					self.corpus_words[word] = 1
				else:
					self.corpus_words[word] += 1

				# agrego el word a la lista de tags
				self.tag_words[data['tag']].extend([word])

		pickle.dump(self.tag_words, open( "tag_words", "wb" ) )
		pickle.dump(self.corpus_words, open( "corpus_words", "wb" ) )

	def load_train(self):

		self.tag_words = pickle.load( open( "tag_words", "rb" ) )
		self.corpus_words = pickle.load( open( "corpus_words", "rb" ) )

	def _read_test_data(self):

		with open("test.csv") as csvfile:
			reader = csv.reader(csvfile, delimiter=";", quotechar='"')
			for i, row in enumerate(reader, 1):
				self.test_data.append(row[1])

	def _read_training_data(self):

		with open(self.traindata_file, encoding="utf-8") as csvfile:
			reader = csv.reader(csvfile, delimiter=";", quotechar='"')
			for i, row in [(i, r) for i, r in enumerate(reader, 1) if r[2]]:
				# print("Reading row {0}..".format(i))
				for c in row[2].split("."):
					self.training_data.append({"tag": c, "sentence": row[1]})

	def tokenize_and_stemm_sentence(self, sentence):
		return [self.stemmer.stem(w.lower()) for w in nltk.word_tokenize(sentence) if w not in stopwords.words(self.languaje)]

	# calculate a score for a given tag
	def calculate_tag_score(self, sentence, tag_name, show_details=True):
		score = 0
		# tokenize each word in our new sentence
		for word in self.tokenize_and_stemm_sentence(sentence):
			# check to see if the stem of the word is in any of our tags
			if word in self.tag_words[tag_name]:
				# treat each word with same weight
				score += 1
				if show_details:
					print ("   match: [%s] %s" % (word.lower(), self.stemmer.stem(word.lower())))
		return score

	# calculate a score for a given tag taking into account word commonality
	def calculate_tag_score_commonality(self, sentence, tag_name, show_details=True):

		score = 0
		# tokenize each word in our new sentence
		for word in self.tokenize_and_stemm_sentence(sentence):
			# check to see if the stem of the word is in any of our tags
			if word in self.tag_words[tag_name]:
				# treat each word with relative weight
				score += (1 / self.corpus_words[word])

				if show_details:
					print ("\n   match: %s (%s)" % (self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
		return score

	# return the tag with highest score for sentence
	def classify(self, sentence):
		high_tag = None
		high_score = 0
		# loop through our tags
		for c in self.tag_words.keys():
			# calculate score of sentence for each tag
			score = self.calculate_tag_score_commonality(sentence, c, show_details=False)
			# keep track of highest score
			if score > high_score:
				high_tag = c
				high_tag = score

		return high_tag, high_score

	# return the tag with highest score for sentence
	def classify_all(self, sentence, score_min=0, max_values=0):
		tags = []
		# loop through our tags
		for c in self.tag_words.keys():
			# calculate score of sentence for each tag
			score = self.calculate_tag_score_commonality(sentence, c, show_details=False)
			if score >= score_min:
				tags.append({"tag": c, "score": score})

		from operator import itemgetter

		newlist = [e for i, e in enumerate(sorted(tags, key=itemgetter('score'), reverse=True)) if  max_values == 0 or i < max_values]
		return newlist



##################################################################################################################################################
# Main program
##################################################################################################################################################
if __name__ == "__main__":

	cmdparser = init_argparse()
	try:
		args = cmdparser.parse_args()
	except IOError as msg:
		cmdparser.error(str(msg))
		sys.exit(-1)

	"""
	O se muestran los formatos o se procesa un archivo
	"""
	if not args.sentence and not args.train_file:
		cmdparser.error("Se debe indicar la sentencia a analizar\n")
		sys.exit(-1)

	if args.train_file:
		clt = TextClasiffier()
		clt.train_from(args.train_file)
		print ("--------------------------------------------------------")
		print ("%s sentences of training data" % len(clt.training_data))
		print ("--------------------------------------------------------")
		sys.exit(0)


	clt = TextClasiffier()
	clt.load_train()

	print ("--------------------------------------------------------")
	print ("Corpus words lenght: %s \n" % len(clt.corpus_words))
	print ("--------------------------------------------------------")


	# we can now calculate a score for a new sentence
	# sentence = "el gasto 55 lo tiene bloqueado ADM. Que hago?"
	# sentence = "Las facturas quedan en emisiÃ³n Las facturas quedan en estado de emisiÃ³n sin recibior autorizaciÃ³n por parte de la AFIP 1-CNG MT"
	# sentence = "Aplicaciones. ProvImg Se reportan problemas cuando dos usuarios intentan scanear al mismo tiempo 1-GPLP PM"
	# sentence = "MAC - Diferencia entre el parte de facturación y el resumen de facturación 18-02-2015 De: Carmen Larreta [mailto:CJLS@marval.com] Enviado el: jueves, 19 de febrero de 2015 08:44 a.m.Para: Emiliano GattiCC: Soporte, Emma Cecilia Di Iorio, Carolina Gómez, Susana R. Enriquez, Ana Maria LupanoAsunto: Diferencia entre el parte de facturación y el resumen de facturación 18-02-2015Buen día: Les informo que hay una diferencia de US$ 1654.61 entre el subtotal de facturación del parte diario (US$ 55.070.60) y el subtotal de facturación del resumen (U$S 53.415.99). Día 18-02-2015. No puedo detectar de dónde surge la diferencia pero puede ser que tenga que ver la factura No. 684 de la cta. Cte. 7439 en $ Pesos. Estimo que el subtotal del parte es el correcto. Por favor se podrían fijar porque tal vez lo que se mandó a Contaduría esté mal. Muchas gracias. Saludos, Carmen Larreta Marval, O'Farrell & MairalAv. Leandro N. Alem 928C1001AAR. Buenos Aires. ArgentinaT. (54-11) 4310-0100 ext. 1427F. (54-11) 4310-0203www.marval.com 1-CJLS EG"
	# sentence = "Error al cargar una cobranza con precobranza Hola Sergio,  mirá el mensaje que me tira,  y no puedo cargar esta precobranza.La necesito cargar para cerrar la caja de ayer. 1-JLL SK"
	# for c in clt.tag_words.keys():
	#     print ("%s -> tag: %s  Score: %s" % (sentence, c, clt.calculate_tag_score(sentence, c)))

	print ("Sentencia: {0}".format(args.sentence))
	print ("--------------------------------------------------------")
	pprint.pprint(clt.classify_all(args.sentence, max_values = 3))
	print ("--------------------------------------------------------")
	# print(stemmer.stem("cierre"))
	# print(stopwords.words('spanish'))
