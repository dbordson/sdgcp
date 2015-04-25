from sdapp.bin import addissuers, formscraper, formparser,\
    populateintermediate, supersedeinit, grabmarketdata,\
    populateformadjustments, populateviews, populatesignals

# This script calls the other executables in proper order to start with a
# list of tickers and build out all the needed filings from an up to date
# filing index in Heroku.  Because you usually won't have an up to date index
# when starting from blank slate in Heroku, this is more for illustrative
# purposes.  The correct order is asfollows, with indications of how each
# script should be run:

# from sdapp.bin import addissuers  # Can run in heroku or locally
# from sdapp.bin import ftpfilelister  # Must be run locally
#       (because it needs access to file indices, which aren't online)
# from sdapp.bin import formscraper  # Can run in heroku or locally
# from sdapp.bin import formparser  # Can run in heroku or locally
# from sdapp.bin import populateintermediate  # Can run in heroku or locally
# from sdapp.bin import supersedeinit  # Can run in heroku or locally
# from sdapp.bin import grabmarketdata  # Can run in heroku or locally
# from sdapp.bin import populateformadjustments  # Can run in heroku or locally
# from sdapp.bin import populateviews  # Can run in heroku or locally

# ** Note: The updatetitles.py script is called from inside the
#          populateintermediates.py script; this is most of the 'securities
#          logic.'
