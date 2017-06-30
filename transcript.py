from collections import OrderedDict
# from operator import itemgetter
import os
from pyth.plugins.plaintext.writer import PlaintextWriter
from pyth.plugins.rtf15.reader import Rtf15Reader
from stopwords import stoplist
import re
import string


class Speaker:
    def __init__(self, tag, filename, isexecutive, isanalyst, wordod,
                 comments):
        # tag
        self.tag = tag
        tag_list = tag.split('\n')
        # filename
        self.filename = filename
        # name
        self.name = tag_list[0].strip()
        # title
        if len(tag_list) > 1:
            self.title = tag_list[1].strip()
        else:
            self.title = None
        # executive
        if isexecutive is True:
            self.executive = True
        else:
            self.executive = False
        # analyst
        if isanalyst is True:
            self.analyst = True
        else:
            self.analyst = False
        # wordod (Ordered Dict of word counts)
        self.wordod = wordod
        # comments (in string)
        self.comments = comments

    def __repr__(self):
        return u'\n%r\n%r\n%r\n%r' % (
            u'Tag: ' + unicode(self.tag).strip(),
            u'Filename: ' + unicode(self.filename),
            u'Top Words: ' + unicode(list(self.wordod.items())[:3]) + '...',
            u'Comments: ' + unicode(self.comments[:50]) + '...'
        )

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
    # print len(transcriptstring)
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
    #
    # Decodes strings
    transcriptstring = transcriptstring.decode('utf-8', 'replace')
    transcriptnopunctuation = deletepunctuation(transcriptstring)
    # transcriptnopunctuation =\
    #     transcriptnopunctuation.decode('utf-8', 'replace')
    # print len(transcriptnopunctuation)
    return transcriptstring, transcriptnopunctuation


def ExtractSpeakers(transcriptstring, startmarker, endmarker):
    startcut = transcriptstring.find(startmarker)+len(startmarker)
    endcut = transcriptstring.find(endmarker)
    speakerstring = transcriptstring[startcut:endcut].strip()
    # print "speakerstring", len(speakerstring)
    speakerlist = map(unicode.strip, speakerstring.split('\n\n'))
    # print "speakerlist", speakerlist
    # speakerlist = map(lambda x: x.split('\n'), speakerlist)
    return speakerlist


def FindLegend(transcriptstring):
    presentationstartmarker = '\n\nPresentation\n........'
    questionandanswermarker = '\n\nQuestion and Answer\n........'
    presentationstartfind =\
        transcriptstring.find(presentationstartmarker)
    questionandanswerfind =\
        transcriptstring.find(questionandanswermarker)
    # Logic below handles situations where call starts w/ Q&A or Presentation
    if presentationstartfind != -1 and questionandanswerfind != -1:
        legendstart = min(presentationstartfind,
                          questionandanswerfind)
        legendend = min(presentationstartfind + len(presentationstartmarker),
                        questionandanswerfind + len(questionandanswermarker))
    elif presentationstartfind == -1 and questionandanswerfind != -1:
        legendstart = questionandanswerfind
        legendend = questionandanswerfind + len(questionandanswermarker)
    elif presentationstartfind != -1 and questionandanswerfind == -1:
        legendstart = presentationstartfind
        legendend = presentationstartfind + len(presentationstartmarker)
    else:
        print "ERROR COULD NOT FIND START OF CALL TRANSCRIPTION"
        legendstart, legendend = 1, 2
    legendendmarker = transcriptstring[legendstart:legendend]
    return legendstart, legendend, legendendmarker


def FindSpeakers(transcriptstring, legendendmarker):
    # legendstartmarker = '\n\n\nCall Participants\n'
    executivestartmarker = '\nEXECUTIVES\n\n'
    analyststartmarker = '\nANALYSTS\n\n'
    operator = '\nOperator'
    #
    # print transcriptstring
    executiveslist =\
        ExtractSpeakers(transcriptstring, executivestartmarker,
                        analyststartmarker)
    # print "executiveslist", len(executiveslist), len(executiveslist[0])
    analystslist =\
        ExtractSpeakers(transcriptstring, analyststartmarker, legendendmarker)
    # print "analystslist", analystslist
    #
    return executiveslist, analystslist, operator


def OrganizeTranscriptBySpeaker(transcriptstring, executiveslist,
                                analystslist, operator, filename,
                                legendend):
    callstring = transcriptstring[legendend:]
    # print "transcriptstring", len(transcriptstring)
    # questionandanswermarker = '\nQuestion and Answer\n.....'
    # callstringlinelist = callstring.split('\n')
    #
    speakerlist = executiveslist + analystslist
    # print "analystslist", analystslist
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
    # print len(commentlist), filename
    # print filteredcomments
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
    document_object = Rtf15Reader.read(open(path + filename, "rb"))
    # string and list objects relating from transcript
    transcriptstring, transcriptnopunctuation = FileProcessor(document_object)
    # find legend start and end which are used to distinguish between speakers
    # section and body of transcript
    legendstart, legendend, legendendmarker = FindLegend(transcriptstring)
    # extract executive, analyst and operator strings used to idenfity speakers
    executiveslist, analystslist, operator =\
        FindSpeakers(transcriptstring, legendendmarker)
    # Next cut transcript string into segments by speaker
    commentlist, aggregatecommentlist =\
        OrganizeTranscriptBySpeaker(transcriptstring, executiveslist,
                                    analystslist, operator, filename,
                                    legendend)
    # Analyze transcript
    # orderedworddict =\
    #     AnalyzeTranscript(transcriptnopunctuation)
    personwordcounts = AnalyzeComments(aggregatecommentlist)
    personobjects = []
    for person in personwordcounts:
        isexecutive = person[0] in executiveslist
        isanalyst = person[0] in analystslist
        personobject =\
            Speaker(
                person[0], filename, isexecutive, isanalyst,
                person[1], person[2]
            )
        personobjects.append(personobject)
    # personobjects = map()
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
    return personobjects


print "Beginning Transcript Analysis"
path = "./transcripts/"
pathcontents = os.listdir(path)
fileinformation = []
nameset = set()
for location in pathcontents:
    if location[-4:] == '.rtf':
        filename = location
        personobjects = reviewfile(path, filename)
        fileinformation.append(personobjects)
        for person in personobjects:
            nameset.add(person.name)
# INSERT NEARMATCH MECHANISM FOR NAMES
print fileinformation
print nameset
