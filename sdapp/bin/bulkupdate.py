# TO RUN THIS IN GCP:
# First run "from sdapp.bin import initialdownload" in a local shell.
# because GCP can't run "initialdownload.py", because it does not appear to
# support FTP access.
from sdapp.bin import formscraper, formparser, populateintermediate,\
    grabmarketdata,\
    populateformadjustments, supersedeinit, adjsharesremaining

from sdapp.bin import update_affiliation_data

from sdapp.bin import newpopulatesigs
