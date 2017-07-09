from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import re

# Do not use this in capitaliq pdfs where there is need to extract date
# information in a collection of multiple calls, because the header/footer
# processing is likely to delete the dates and call descriptions.

# converts pdf, returns its text content as a string


def convert(fname):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    pdftext = output.getvalue()
    output.close
    return pdftext


fname = 'data/MSFT Transcript Digest.pdf'
pdftext = convert(fname)
print 'converted text string length is', len(pdftext)
# regex pattern for that URL with up to 300 characters followed by year date
# after 2000 at end of line.  The re.DOTALL method causes the r'.' to include
# newline characters in the character gap.
p = re.compile(r'WWW.SPCAPITALIQ.COM'+r'.{1,300}'+r'\b20\d{2}\n', re.DOTALL)
lengthfoundsubs = len(''.join(p.findall(pdftext)))
print 'found subs text string length is', lengthfoundsubs
print 'length of converted text minus found subs is', len(pdftext)\
    - lengthfoundsubs
cleanedpdftext = pdftext
cleanedpdftext = p.sub('', cleanedpdftext)
print 'cleaned text string length is', len(cleanedpdftext)
