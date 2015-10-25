from django.conf import settings
from django.contrib.auth.models import User
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from sdapp.bin.globals import app_url
from sdapp.models import WatchedName, SigDisplay

import os


def signalemail(new_signal_user, watched_signals, app_url):
    user = new_signal_user
    sigdisplays = watched_signals
    if sigdisplays.count() == 1:
        sigdisplay_for_email = sigdisplays[0]
        name = sigdisplay_for_email.issuer.name.strip()
        if name[-1] != '.':
            endline = '.'
        else:
            endline = ''
        link = app_url + sigdisplay_for_email.sec_price_hist.ticker_sym
        subject = 'New Insider Signal - %s' % name
        textbody = 'We have detected a new signal for %s' % name\
            + endline + os.linesep + os.linesep\
            + 'See this link for details: ' + link + os.linesep + os.linesep\
            + 'Regards, [TEAM NAME]'
        htmlbody =\
            get_template('single_signal_message.html')\
            .render(Context({'name': name,
                             'endline': endline,
                             'app_url': app_url,
                             'ticker': sigdisplay_for_email.sec_price_hist
                             .ticker_sym}))

    elif sigdisplays.count() > 1:
        subject = 'New Insider Signals'
        textbody = 'We have detected %d new signals:' % sigdisplays.count()\
            + os.linesep
        for sigdisplay in sigdisplays:
            textbody += sigdisplay.sec_price_hist.ticker_sym + ' - '\
                + 'See this link for details: ' + app_url\
                + sigdisplay.sec_price_hist.ticker_sym + os.linesep\
                + os.linesep

        textbody += os.linesep + 'Regards, [TEAM NAME]'
        htmlbody =\
            get_template('multi_signal_message.html')\
            .render(Context({'sig_count': sigdisplays.count(),
                             'sigdisplays': sigdisplays,
                             'app_url': app_url}))

    else:
        print 'ERROR signalemail function run with an empty queryset'
        print 'error user:', user
        return

    from_email = settings.EMAIL_HOST_USER
    to_list = [User.objects.get(pk=user).email]
    msg = EmailMultiAlternatives(subject, textbody, from_email, to_list)
    msg.attach_alternative(htmlbody, "text/html")
    msg.send()

    # send_mail(subject, textbody, from_email, to_list, fail_silently=True)
    return


print 'Sorting new signals, tickers, users...'
new_sig_disp =\
    SigDisplay.objects.filter(signal_is_new=True)
new_sig_issuers =\
    new_sig_disp.values_list('issuer', flat=True).distinct()
watched_names_with_new_signal =\
    WatchedName.objects.filter(issuer__in=new_sig_issuers)
new_signal_users =\
    watched_names_with_new_signal.values_list('user', flat=True)\
    .distinct()
'...sending emails...'
for new_signal_user in new_signal_users:
    user_issuers =\
        watched_names_with_new_signal.filter(user=new_signal_user)\
        .values_list('issuer', flat=True)
    watched_signals =\
        new_sig_disp.filter(issuer__in=user_issuers)\
        .order_by('issuer__name')
    signalemail(new_signal_user, watched_signals, app_url)

'...Done.'
