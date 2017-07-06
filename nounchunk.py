import spacy
from collections import Counter, defaultdict

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().decode('utf-8')


nlp = spacy.load('en')

transcript = read_file('data/2017Q3.txt')
processed_transcript = nlp(transcript)


keywords = Counter()
for chunk in processed_transcript.noun_chunks:
    # probablity value -8 is arbitrarily selected threshold based on sample
    # https://github.com/cytora/pycon-nlp-in-10-lines/blob/master/01_pride_and_predjudice.ipynb
    # I don't yet totally understand what the probabilities represent, but I
    # note they are the log of the proability which means each probability is a
    # tiny number (i.e. log(.00000001) = -8).
    if nlp.vocab[chunk.lemma_].prob < - 8:
        keywords[chunk.lemma_] += 1

for word, count in keywords.most_common():
    print word, count
