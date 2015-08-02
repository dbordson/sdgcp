from sdapp.models import Form345Entry

from sdapp.bin import supersedetools as st

# INTRO NOTE:
# It is critical, based on how the logic works, to avoid doing anything
# while this script runs that could change an entry's primary key (perhaps
# vacuum could do this?) if this becomes a problem, we could use the
# entry_internal_id for each entry, but this will probably be much slower.

print 'Calculating superseded dates of unsuperseded forms...'
unique_security_chains =\
    list(Form345Entry.objects
         .filter(supersededdt=None)
         .values_list('affiliation', 'short_sec_title',
                      'expiration_date', 'direct_or_indirect')
         .distinct())

looplength = float(len(unique_security_chains))
counter = 0.0

for affiliation, short_sec_title, expiration_date,\
        direct_or_indirect in unique_security_chains:

    if float(int(20*counter/looplength)) !=\
            float(int(20*(counter-1)/looplength)):
        print int(counter/looplength*100), 'percent'
    counter += 1.0

    st.calc_supersededdts_for_chains(affiliation,
                                     short_sec_title, expiration_date,
                                     direct_or_indirect)
    if counter % 1000.0 == 0:
        st.reset_database_connection()
print '...Done with general case...'
# Now superseding officers who disappeared with entries on the books
print 'Now superseding former officers with stale forms...'
officercutoffyears = 2
is_officer = True
st.supersede_stale_entries(officercutoffyears, is_officer)
print '...Done with officers...'
# Now superseding nonofficers who disappeared with entries on the books
print 'Now superseding former nonofficers with stale forms...'
nonofficercutoffyears = 5
is_officer = False
st.supersede_stale_entries(nonofficercutoffyears, is_officer)
print '...Done with nonofficers...'
print '...Done with superseded dates script.'
