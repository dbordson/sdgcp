# Totally fine to run this in heroku.
from sdapp.models import Form345Entry
from sdapp.bin import updatedownload, formscraper, formparser

affiliations_to_update = \
    list(Form345Entry.objects.filter(affiliation=None)
         .values_list('issuer_cik', 'reporting_owner_cik_num').distinct())
# print affiliations_to_update
from sdapp.bin import populateintermediate, supersedeinit, adjsharesremaining,\
    grabmarketdata, populateformadjustments

from sdapp.bin import update_affiliation_data

update_affiliation_data.update(affiliations_to_update)
update_affiliation_data.calc_percentiles()

from sdapp.bin import populateviews, newpopulatesigs
