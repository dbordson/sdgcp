from sdapp.bin import updatedownload, formscraper
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
