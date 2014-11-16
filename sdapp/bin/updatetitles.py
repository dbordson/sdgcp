from sdapp.models import Form345Entry
from django.db.models import Q


def update_short_titles():
    print 'Adding new short_sec_title and scrubbed_underlying_title fields to',
    print 'Form345Entry objects...'
    print '    Sorting, linking and saving...',

    issuer_ciks_with_forms_missing_short_titles =\
        set(Form345Entry.objects.filter(short_sec_title=None)
            .values_list('issuer_cik_num', flat=True))
    for issuer_cik in issuer_ciks_with_forms_missing_short_titles:
        multiple_classes_of_common = False
# The below script involves some pretty complex queries, but it basically
# tries to determine whether a named condition is present (e.g. multiple
# classes of common) and then it gives sensible short names based on the
# condition.  It treats both security titles and also underlying security
# titles (for derivatives) in an attempt to keep these consistently named.
# The queries below look quite similar, but they are not indentically
# structured.  This was an attempt at aligning queries with conceptual
# between categories.

# Common Stock Naming
        if Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(Q(security_title__icontains='class b') |
                        Q(security_title__icontains='class c') |
                        Q(security_title__icontains='class d'))\
                .exclude(security_title__icontains='preferred')\
                .exclude(security_title__icontains='unit')\
                .exclude(security_title__icontains='option')\
                .exclude(security_title__icontains='rsu').exists():
            multiple_classes_of_common = True
        if multiple_classes_of_common:
            # Security titles
            forms_for_assignment = \
                Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .filter(Q(security_title__icontains='common') |
                        Q(security_title__icontains='stock'))\
                .exclude(security_title__icontains='preferred')\
                .exclude(security_title__icontains='unit')\
                .exclude(security_title__icontains='option')\
                .exclude(security_title__icontains='rsu')
            for form in forms_for_assignment:
                if 'class' not in form.security_title.lower():
                    form.short_sec_title = 'common stock'
                elif 'class a' in form.security_title.lower():
                    form.short_sec_title = 'class a common stock'
                elif 'class b' in form.security_title.lower():
                    form.short_sec_title = 'class b common stock'
                elif 'class c' in form.security_title.lower():
                    form.short_sec_title = 'class c common stock'
                elif 'class d' in form.security_title.lower():
                    form.short_sec_title = 'class d common stock'
                else:
                    form.short_sec_title = form.security_title.lower()
                form.save()
            # Underlying titles
            forms_for_assignment = \
                Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(scrubbed_underlying_title=None)\
                .filter(Q(underlying_title__icontains='common') |
                        Q(underlying_title__icontains='stock'))\
                .exclude(underlying_title__icontains='preferred')\
                .exclude(underlying_title__icontains='unit')\
                .exclude(underlying_title__icontains='option')\
                .exclude(underlying_title__icontains='rsu')
            for form in forms_for_assignment:
                if 'class' not in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'common stock'
                elif 'class a' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class a common stock'
                elif 'class b' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class b common stock'
                elif 'class c' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class c common stock'
                elif 'class d' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class d common stock'
                else:
                    form.scrubbed_underlying_title =\
                        form.underlying_title.lower()
                form.save()
        else:
            # Security titles
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .filter(Q(security_title__icontains='common') |
                        Q(security_title__icontains='stock'))\
                .exclude(security_title__icontains='preferred')\
                .exclude(security_title__icontains='unit')\
                .exclude(security_title__icontains='option')\
                .exclude(security_title__icontains='rsu')\
                .update(short_sec_title='common stock')
            # Underlying titles
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(scrubbed_underlying_title=None)\
                .filter(Q(underlying_title__icontains='common') |
                        Q(underlying_title__icontains='stock'))\
                .exclude(underlying_title__icontains='preferred')\
                .exclude(underlying_title__icontains='unit')\
                .exclude(underlying_title__icontains='rsu')\
                .update(scrubbed_underlying_title='common stock')

# Preferred Stock Naming
        multiple_classes_of_preferred = False
        if Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(security_title__icontains='preferred')\
                .filter(Q(security_title__icontains='class b') |
                        Q(security_title__icontains='class c') |
                        Q(security_title__icontains='class d') |
                        Q(security_title__icontains='series b') |
                        Q(security_title__icontains='series c') |
                        Q(security_title__icontains='series d'))\
                .exclude(security_title__icontains='common')\
                .exclude(security_title__icontains='convertible')\
                .exclude(security_title__icontains='option')\
                .exists():
            multiple_classes_of_preferred = True

        if multiple_classes_of_preferred:
            # Security titles
            forms_for_assignment = \
                Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .exclude(security_title__icontains='option')\
                .exclude(security_title__icontains='convertible')\
                .filter(security_title__icontains='preferred')
            for form in forms_for_assignment:
                if 'class' not in form.security_title.lower()\
                        and 'series' not in form.security_title.lower():
                    form.short_sec_title = 'preferred stock'
                elif 'class a' in form.security_title.lower():
                    form.short_sec_title = 'class a preferred stock'
                elif 'class b' in form.security_title.lower():
                    form.short_sec_title = 'class b preferred stock'
                elif 'class c' in form.security_title.lower():
                    form.short_sec_title = 'class c preferred stock'
                elif 'class d' in form.security_title.lower():
                    form.short_sec_title = 'class d preferred stock'
                elif 'series a' in form.security_title.lower():
                    form.short_sec_title = 'series a preferred stock'
                elif 'series b' in form.security_title.lower():
                    form.short_sec_title = 'series b preferred stock'
                elif 'series c' in form.security_title.lower():
                    form.short_sec_title = 'series c preferred stock'
                elif 'series d' in form.security_title.lower():
                    form.short_sec_title = 'series d preferred stock'
                else:
                    form.short_sec_title = form.security_title.lower()
                form.save()
            # Underlying titles
            forms_for_assignment = \
                Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(scrubbed_underlying_title=None)\
                .exclude(underlying_title__icontains='option')\
                .exclude(underlying_title__icontains='convertible')\
                .filter(underlying_title__icontains='preferred')
            for form in forms_for_assignment:
                if 'class' not in form.underlying_title.lower()\
                        and 'series' not in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'preferred stock'
                elif 'class a' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class a preferred stock'
                elif 'class b' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class b preferred stock'
                elif 'class c' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class c preferred stock'
                elif 'class d' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'class d preferred stock'
                elif 'series a' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'series a preferred stock'
                elif 'series b' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'series b preferred stock'
                elif 'series c' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'series c preferred stock'
                elif 'series d' in form.underlying_title.lower():
                    form.scrubbed_underlying_title = 'series d preferred stock'
                else:
                    form.scrubbed_underlying_title =\
                        form.underlying_title.lower()
                form.save()
        else:
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .filter(security_title__icontains='preferred')\
                .exclude(security_title__icontains='convertible')\
                .update(short_sec_title='preferred stock')
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(scrubbed_underlying_title=None)\
                .filter(underlying_title__icontains='preferred')\
                .exclude(underlying_title__icontains='convertible')\
                .update(scrubbed_underlying_title='preferred stock')
# Restricted Stock Units
        if Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .exclude(security_title__icontains='option')\
                .filter(Q(security_title__contains='RSU') |
                        Q(security_title__icontains='restricted stock unit'))\
                .exists():
            # Non-derivative
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(short_sec_title=None)\
                .exclude(security_title__icontains='option')\
                .filter(Q(security_title__contains='RSU') |
                        Q(security_title__icontains='restricted stock unit'))\
                .update(short_sec_title='restricted stock units')
            # Derivative
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(scrubbed_underlying_title=None)\
                .exclude(underlying_title__icontains='option')\
                .filter(Q(underlying_title__icontains='RSU') |
                        Q(underlying_title__icontains='restricted stock unit')
                        )\
                .exclude(underlying_title=None)\
                .update(scrubbed_underlying_title='restricted stock units')
# Stock options
        put_options_present = False
        if Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(deriv_or_nonderiv='D')\
                .filter(short_sec_title=None)\
                .filter(Q(security_title__icontains='right to sell') |
                        Q(security_title__icontains='put option'))\
                .exists():
            put_options_present = True
        if put_options_present:
            forms_for_assignment = \
                Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(deriv_or_nonderiv='D')\
                .filter(short_sec_title=None)\
                .filter(Q(security_title__icontains='option') |
                        Q(security_title__icontains='to sell') |
                        Q(security_title__icontains='to buy') |
                        Q(security_title__icontains='put option') |
                        Q(security_title__icontains='call option'))
            for form in forms_for_assignment:
                if 'call' in form.security_title.lower():
                    form.short_sec_title = 'call option'
                elif 'put' in form.security_title.lower():
                    form.short_sec_title = 'put option'
                elif 'to buy' in form.security_title.lower():
                    form.short_sec_title = 'call option'
                elif 'to sell' in form.security_title.lower():
                    form.short_sec_title = 'put option'
                else:
                    form.short_sec_title = 'call option'
                form.save()
        else:
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
                .filter(deriv_or_nonderiv='D')\
                .filter(short_sec_title=None)\
                .filter(Q(security_title__icontains='option') |
                        Q(security_title__icontains='to buy'))\
                .update(short_sec_title='call option')

        remaining_sec_title_forms =\
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
            .exclude(security_title=None)\
            .filter(short_sec_title=None)
        for form in remaining_sec_title_forms:
            form.short_sec_title = form.security_title.lower()
            form.save()
        remaining_underlying_title_forms =\
            Form345Entry.objects.filter(issuer_cik_num=issuer_cik)\
            .filter(scrubbed_underlying_title=None)\
            .exclude(underlying_title=None)
        for form in remaining_underlying_title_forms:
            form.scrubbed_underlying_title = form.underlying_title.lower()
            form.save()
    print 'done.'
