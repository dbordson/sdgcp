from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from sdapp.models import Signal, WatchedName

import os

def signalemail(new_signal_user, user_signals):
    app_url = 'http://127.0.0.1:8000/sdapp/'
    user = new_signal_user
    signals = user_signals
    if signals.count() == 1:
        signal_for_email = signals[0]
        name = signal_for_email.issuer.name.strip()
        if name[-1] != '.':
            endline = '.'
        else:
            endline = ''
        link = app_url + signal_for_email.sph.ticker_sym
        subject = 'New Insider Signal - %s' % name
        textbody = 'We have detected a new signal for %s' % name\
            + endline + os.linesep + os.linesep\
            + signal_for_email.long_statement + os.linesep + os.linesep\
            + 'See this link for details: ' + link + os.linesep + os.linesep\
            + 'Regards, [TEAM NAME]'
        htmlbody =\
            get_template('single_signal_message.html')\
            .render(Context({'name': name,
                             'endline': endline,
                             'sig_statement': signal_for_email.long_statement,
                             'app_url': app_url,
                             'ticker': signal_for_email.sph.ticker_sym}))

    elif signals.count() > 1:
        subject = 'New Insider Signals'
        textbody = 'We have detected %d new signals:' % signals.count()\
            + os.linesep
        for signal in signals:
            textbody += signal.sph.ticker_sym + ' - ' + signal.short_statement\
                + '.' + os.linesep + 'See this link for details: '\
                + app_url + signal.sph.ticker_sym + os.linesep + os.linesep

        textbody += os.linesep + 'Regards, [TEAM NAME]'
        htmlbody =\
            get_template('multi_signal_message.html')\
            .render(Context({'sig_count': signals.count(),
                             'signals': signals,
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
new_signals =\
    Signal.objects.exclude(sph=None)\
    .filter(signal_is_new=True)
tickers =\
    new_signals.values_list('sph__ticker_sym', flat=True).distinct()
watched_names_with_new_signal =\
    WatchedName.objects.filter(ticker_sym__in=tickers)
new_signal_users =\
    watched_names_with_new_signal.values_list('user', flat=True)\
    .distinct()
'...sending emails...'
for new_signal_user in new_signal_users:
    user_tickers =\
        watched_names_with_new_signal.filter(user=new_signal_user)\
        .values_list('ticker_sym', flat=True)
    user_signals =\
        new_signals.filter(sph__ticker_sym__in=user_tickers)\
        .order_by('sph__ticker_sym', 'signal_date')
    signalemail(new_signal_user, user_signals)

'...Done.'
