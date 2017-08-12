import spacy

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter


def extractstringfromRTF(path, filename):
    document_object = Rtf15Reader.read(open(path + filename, "rb"))
    transcriptstring = PlaintextWriter.write(document_object).read()
    return transcriptstring


filename = '2017Q3 Finisar Corp.rtf'
path = 'transcripts/'
transcriptstring = extractstringfromRTF(path, filename)
unicodetext = transcriptstring.decode('utf-8', 'replace')
len(unicodetext)
textlist = unicodetext.split(' ')
filteredtextlist = filter(lambda x: len(x) < 400, textlist)
filteredtext = ' '.join(filteredtextlist)

nlp = spacy.load('en')
doc = nlp(filteredtext)
sents = []
for x in doc.sents:
    sents.append(x)
