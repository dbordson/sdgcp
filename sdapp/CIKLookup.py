import requests
# This requires requests, which can be installed via pip using "pip install requests" (http://docs.python-requests.org/en/latest/user/install/#install for info)
def CIKFind(ticker):

	url = 'http://www.sec.gov/cgi-bin/browse-edgar?company=&match=&CIK=%s&owner=exclude&Find=Find+Companies&action=getcompany' % ticker
	starttag = 'CIK='
	endtag = '&amp'

	try:
		response = requests.get(url)
		CIKstart = response.text.find(starttag)
		CIKend = response.text.find(endtag, CIKstart)
		CIK = response.text[CIKstart + len(starttag):CIKend]
	except:
		CIK = 'ACCESS ERROR'

	if len(CIK) > 11:
		CIK = 'NO CIK FOUND'

	return CIK

source = open("S&P Ticker List.txt")

#The below file is where the results will go
target = open("CIKList.txt", 'w')

tickerlines = source.readlines()

for line in tickerlines:
	tickerend = line.find('\t')
	ticker = line[:tickerend].replace('.','')
	name = line[tickerend+1:]
	line.strip()
	#print line.find("\t")

	target.write(CIKFind(ticker) + '  ' + ticker + '  ' + name)

source.close()
target.close()

print "Done.  Check CIKList.txt in this folder for results."
