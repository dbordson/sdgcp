# TO RUN THIS IN HEROKU:
# First run "from sdapp.bin import initialdownload" in a local shell.
# because heroku can't run "initialdownload.py", because indices not stored
# in heroku.
from sdapp.bin import updatedownload, formscraper, formparser,\
    populateintermediate, supersedeinit, adjsharesremaining,\
    grabmarketdata,\
    populateformadjustments, populateviews, populatesignals,\
    populaterecommendations
