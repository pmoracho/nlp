# -*- coding: utf-8 -*-

# Copyright (c) 2014 Patricio Moracho <pmoracho@gmail.com>
#
# ArBooks
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

import re
import os
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import *
from nltk.text import Text
# from nltk.probability import FreqDist
# from nltk.util import bigrams

root_path = os.path.dirname(os.path.realpath(__file__))

ar_books = LazyCorpusLoader('ar.books',
							PlaintextCorpusReader, r'(?!\.).*\.txt',
							encoding='utf-8',
							nltk_data_subdir=os.path.join(root_path,"corpora"))



print("*** Ejemplos de Literatura Argentina bajo dominio público ***")
print("Loading text1, ..., text6")
print("Type the name of the text or sentence to view it.")
print("Type: 'texts()' or 'sents()' to list the materials.")

text1 = Text(ar_books.words('facundo.txt'));print("text1:", text1.name)
text2 = Text(ar_books.words('el.juguete.rabioso.txt'));print("text2:", text2.name)
text3 = Text(ar_books.words('el.matadero.txt'));print("text3:", text3.name)
text4 = Text(ar_books.words('juvenillia.txt'));print("text4:", text4.name)
text5 = Text(ar_books.words('los.desterrados.txt'));print("text5:", text5.name)
text6 = Text(ar_books.words('cuentos.de.amor.locura.y.de.muerte.txt'));print("text6:", text6.name)

def texts():
    print("text1:", text1.name)
    print("text2:", text2.name)
    print("text3:", text3.name)
    print("text4:", text4.name)
    print("text5:", text5.name)
    print("text6:", text6.name)

sent1 = ["Era", "el", "martes", "de", "carnaval"]
sent2 = ["A", "fines", "del", "año", "1840", "salía", "yo", "de", "mi", "patria"]
sent3 = ["Era", "el", "martes", "de", "carnaval"]
sent4 = ["Era", "el", "martes", "de", "carnaval"]
sent5 = ["Era", "el", "martes", "de", "carnaval"]
sent6 = ["Era", "el", "martes", "de", "carnaval"]


def sents():
    print("sent1:", " ".join(sent1))
    print("sent2:", " ".join(sent2))
    print("sent3:", " ".join(sent3))
    print("sent4:", " ".join(sent4))
    print("sent5:", " ".join(sent5))
    print("sent6:", " ".join(sent6))

if __name__ == '__main__':
	ar = ar_books
	print(ar)
	print(ar.words())
	print(text1)
