from collections import OrderedDict
# from operator import itemgetter
import os
from pyth.plugins.plaintext.writer import PlaintextWriter
from pyth.plugins.rtf15.reader import Rtf15Reader
from stopwords import stoplist
import re
import string


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def deletepunctuation(stringwithpunctuation):
    # Removes punctuation
    punctuation = unicode(string.punctuation)
    translate_table = dict((ord(char), u' ') for char in punctuation)
    stringwithoutpunctuation =\
        stringwithpunctuation.translate(translate_table)
    #
    return stringwithoutpunctuation


def FileProcessor(document_object):
    transcriptstring = PlaintextWriter.write(document_object).read()
    #
    # Removes non-text information from transcriptstring
    transcriptstring = re.sub(r'\b\w{50,}\b', '', transcriptstring)
    #
    # Removes trailing spaces for each line in transcriptstring
    transcriptstring =\
        ''.join([line.rstrip()+'\n' for line in transcriptstring.splitlines()])
    #
    # Removes disclaimer at endcut
    callendmarker = '\n\n\n\n\n\n\n\n\n\n\n\n\n'
    endcut = transcriptstring.find(callendmarker)
    if endcut is not -1:
        transcriptstring = transcriptstring[:endcut]
    #
    # Strips out certain escape characters that don't seem to get handled above
    # Below doesn't work properly because it also deletes all "s" characters
    # escchars = '\xc2\xa9\xe2\x80\x99s'
    # replace_esc = string.maketrans(escchars,
    #                                ' '*len(escchars))
    # transcriptstring = transcriptstring.translate(replace_esc)
    #
    transcriptnopunctuation = deletepunctuation(unicode(transcriptstring))
    #
    # Decodes strings
    transcriptstring = transcriptstring.decode('utf-8')
    transcriptnopunctuation.decode('utf-8')
    #
    return transcriptstring, transcriptnopunctuation


def ExtractSpeakers(transcriptstring, startmarker, endmarker):
    startcut = transcriptstring.find(startmarker)+len(startmarker)
    endcut = transcriptstring.find(endmarker)
    speakerstring = transcriptstring[startcut:endcut].strip()
    speakerlist = map(unicode.strip, speakerstring.split('\n\n'))
    # speakerlist = map(lambda x: x.split('\n'), speakerlist)
    return speakerlist


def FindSpeakers(transcriptstring, legendendmarker):
    legendstartmarker = '\n\n\nCall Participants\n'
    executivestartmarker = '\nEXECUTIVES\n\n'
    analyststartmarker = '\nANALYSTS\n\n'
    operator = '\nOperator'
    #
    executiveslist =\
        ExtractSpeakers(transcriptstring, executivestartmarker,
                        analyststartmarker)
    analystslist =\
        ExtractSpeakers(transcriptstring, analyststartmarker, legendendmarker)
    #
    return executiveslist, analystslist, operator


def OrganizeTransacriptBySpeaker(transcriptstring, executiveslist,
                                 analystslist, operator):
    callstartmarker = '\n\nPresentation\n........'
    startcut = transcriptstring.find(callstartmarker)+len(callstartmarker)
    callstring = transcriptstring[startcut:]
    # questionandanswermarker = '\nQuestion and Answer\n.....'
    # callstringlinelist = callstring.split('\n')
    #
    speakerlist = executiveslist + analystslist
    speakerlist.append(operator)
    speakerlocations =\
        map(lambda x: [[x, m.start(), m.end()]
                       for m in re.finditer(x, callstring)], speakerlist)
    # Removes nesting
    speakerlocations = [comment for speaker in speakerlocations
                        for comment in speaker]
    # sorts list
    speakerlocations = sorted(speakerlocations, key=lambda comment: comment[1])
    speakerlocations.append([u'', len(callstring)-1, None])
    # for lineitem in callstringlinelist:
    #     if lineitem
    commentlist = []
    #
    for i in range(0, len(speakerlocations)-1):
        commentlist.append([
            speakerlocations[i][0],
            speakerlocations[i][1],
            speakerlocations[i][2],
            speakerlocations[i+1][1],
            callstring[speakerlocations[i][2]:speakerlocations[i+1][1]].strip()
        ])
    # Put all comments for each person in one string
    # organize comments by speaker
    filteredcomments =\
        map(lambda y: filter(lambda x: x[0] == y, commentlist), speakerlist)
    # The below line is tricky -- it cuts apart the comments by speaker and
    # extracts the speaker and the comments (which is zip(*x)[4]) and joins the
    # comments
    aggregatecommentlist =\
        map(lambda x: [x[0][0], '\n'.join(zip(*x)[4])], filteredcomments)
    #
    return commentlist, aggregatecommentlist


def AnalyzeTranscript(transcriptnopunctuation):
    stringlist = transcriptnopunctuation.lower().split()
    wordfreq = []
    wordlist = []
    worddict = {}
    for w in stringlist:
        if w not in stoplist and is_number(w) is False:
            wordlist.append(w)
            wordfreq.append(wordlist.count(w))
            worddict[w] = wordlist.count(w)
    orderedworddict =\
        OrderedDict(sorted(worddict.items(),
                    key=lambda x: x[1], reverse=True))
    return orderedworddict


def AnalyzeComments(aggregatecommentlist):
    # aggregatecommentsnopunctuation =\
    #     map(lambda x: [x[0], deletepunctuation(x[1])], aggregatecommentlist)
    personwordcounts = []
    for person, comment in aggregatecommentlist:
        commentnopunctuation = deletepunctuation(comment)
        commentnopunctuationlist = commentnopunctuation.lower().split()
        worddict = {}
        wordlist = []
        for w in commentnopunctuationlist:
            if w not in stoplist and is_number(w) is False:
                wordlist.append(w)
                worddict[w] = wordlist.count(w)
        orderedworddict =\
            OrderedDict(sorted(worddict.items(),
                        key=lambda x: x[1], reverse=True))
        personwordcounts.append([person, orderedworddict, comment])
    return personwordcounts


def reviewfile(path, filename):
    legendendmarker = 'Presentation\n'
    document_object = Rtf15Reader.read(open(path + filename, "rb"))
    # string and list objects relating from transcript
    transcriptstring, transcriptnopunctuation = FileProcessor(document_object)
    # extract executive, analyst and operator strings used to idenfity speakers
    executiveslist, analystslist, operator =\
        FindSpeakers(transcriptstring, legendendmarker)

    # Next cut transcript string into segments by speaker
    commentlist, aggregatecommentlist =\
        OrganizeTransacriptBySpeaker(transcriptstring, executiveslist,
                                     analystslist, operator)
    # Analyze transcript
    # orderedworddict =\
    #     AnalyzeTranscript(transcriptnopunctuation)
    personwordcounts = AnalyzeComments(aggregatecommentlist)
    # print "AGGREGATE COMMENTS ORGANIZED BY EACH PERSON"
    # for person, count, comment in personwordcounts:
    #     print "Speaker:"
    #     print person
    #     print ""
    #     print "Word Count:"
    #     print count
    #     print ""
    #     print "All Comments of Speaker:"
    #     print comment
    #     print ""
    #     print ""
    #     print ""
    return personwordcounts


print "Beginning Transcript Analysis"
path = "./transcripts/"
pathcontents = os.listdir(path)
filewordcounts = []
for location in pathcontents:
    if location[-4:] == '.rtf':
        filename = location
        personwordcounts = reviewfile(path, filename)
        filewordcounts.append(personwordcounts)

print filewordcounts
