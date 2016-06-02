# TO RUN THIS IN GCP:
# First run "from sdapp.bin import updatedownload, formscraper" in a local
# shell, Because GCP can't run "updatedownload.py" or formscraper.py,
# because GCP does not appear to support FTP access.

from sdapp.bin import formparser
from sdapp.models import Form345Entry
affiliations_to_update = \
    list(Form345Entry.objects.filter(affiliation=None)
         .values_list('issuer_cik', 'reporting_owner_cik_num').distinct())
# print affiliations_to_update
from sdapp.bin import populateintermediate, grabmarketdata,\
    populateformadjustments, supersedeinit, adjsharesremaining

from sdapp.bin import update_affiliation_data

from sdapp.bin import newpopulatesigs
