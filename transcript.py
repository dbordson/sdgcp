from collections import OrderedDict
from pyth.plugins.plaintext.writer import PlaintextWriter
from pyth.plugins.rtf15.reader import Rtf15Reader
import re
import string

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'll', 'ltd']
stopwords += ['made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill']
stopwords += ['mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']


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
    # Removes punctuation
    replace_punctuation = string.maketrans(string.punctuation,
                                           ' '*len(string.punctuation))
    transcriptnopunctuation = transcriptstring.translate(replace_punctuation)
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
    operator = '\nOperator\n'
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
    # ADD OTHER SPEAKERS BESIDES MANAGEMENT (ANALYSTS and OPERATOR)
    for i in range(0, len(speakerlocations)-1):
        commentlist.append([
            speakerlocations[i][0],
            speakerlocations[i][1],
            speakerlocations[i][2],
            speakerlocations[i+1][1],
            callstring[speakerlocations[i][2]:speakerlocations[i+1][1]].strip()
        ])
    return commentlist


def AnalyzeTranscript(transcriptnopunctuation):
        stringlist = transcriptnopunctuation.split()
        wordfreq = []
        wordlist = []
        worddict = {}
        for w in stringlist:
            if w not in stopwords:
                wordlist.append(w)
                wordfreq.append(wordlist.count(w))
                worddict[w] = wordlist.count(w)
        orderedworddict =\
            OrderedDict(sorted(worddict.items(),
                        key=lambda x: x[1], reverse=True))
        return transcriptstring, worddict, orderedworddict


filename = 'Finisar.rtf'
legendendmarker = 'Presentation\n'

document_object = Rtf15Reader.read(open(filename, "rb"))
# string and list objects relating from transcript
transcriptstring, transcriptnopunctuation = FileProcessor(document_object)
# extract executive, analyst and operator strings used to idenfity speakers
executiveslist, analystslist, operator =\
    FindSpeakers(transcriptstring, legendendmarker)

# Next cut transcript string into segments by speaker
organizedtranscript =\
    OrganizeTransacriptBySpeaker(transcriptstring, executiveslist,
                                 analystslist, operator)


# Analyze transcript
transcriptstring, worddict, orderedworddict =\
    AnalyzeTranscript(transcriptnopunctuation)
