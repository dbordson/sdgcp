from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext

from sdapp.models import SecurityPriceHist, Signal, WatchedName


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c,
                              context_instance=RequestContext(request))


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        # The below is probably not the right way to do this because it isn't
        # clean, but it works for now.
        if 'HTTP_REFERER' in request.META \
                and request.META['HTTP_REFERER'].find('/?next=/') != -1:
            source_url = request.META['HTTP_REFERER']
            redirect = \
                source_url[source_url.find('/?next=/')+len('/?next=/')-1:]
        else:
            redirect = '/sdapp/'
        return HttpResponseRedirect(redirect)
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('loggedin.html',
                              {'username': request.user.username},
                              context_instance=RequestContext(request),
                              )


def invalid_login(request):
    return render_to_response('invalid_login.html',
                              context_instance=RequestContext(request),
                              )


def changepwloggedout(request):

    return render_to_response('changepwloggedout.html',
                              {'username': request.user.username},
                              context_instance=RequestContext(request),
                              )


def pwresetloggedoutemail(request):
    email = request.POST.get('email', '')
    subject = 'Temporary [PRODUCT NAME] Password'
    new_pw = User.objects.make_random_password()

    message =\
        'We received your password reset request for [PRODUCT NAME].\n\n'\
        + 'Your new password is %s and we suggest that you reset this to '\
        % new_pw\
        + 'something easier to remember. If you did not request a '\
        + 'password reset, please contact us at [SUPPORT EMAIL ADDRESS].\n\n'\
        + 'If you have any questions, feel free to reply to this email.\n\n'\
        + 'Regards,\n'\
        + '[COMPANY NAME] Support'
    from_email = settings.EMAIL_HOST_USER
    # request.user.email
    to_list = [email]
    # print User.objects.filter(email=email)
    if User.objects.filter(email=email).exists():
        u = User.objects.get(email=email)
    else:
        messagetext = \
            'We do not have the email address "%s" on file.  ' % email\
            + 'If this email address is correct, '\
            + 'please contact [SUPPORT EMAIL ADDRESS]'
        messages.warning(request, messagetext)
        return HttpResponseRedirect('/changepwlo/')
    u.set_password(new_pw)
    u.save()
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    print message

    messagetext = \
        'You should receive a new temporary password shortly.'
    messages.warning(request, messagetext)
    return HttpResponseRedirect('/changepwlo/')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html',
                              context_instance=RequestContext(request),
                              )


@login_required()
def accountinfo(request):

    return render_to_response('accountinfo.html',
                              {'username': request.user.username},
                              context_instance=RequestContext(request),
                              )


@login_required()
def changepw(request):

    return render_to_response('changepw.html',
                              {'username': request.user.username},
                              context_instance=RequestContext(request),
                              )


@login_required()
def managewatchlist(request):
    watchlist = \
        WatchedName.objects.filter(user=request.user).order_by('ticker_sym')
    found_sph = None
    ticker_query = None
    already_exists = False
    found_ticker = None
    search = False
    if ('q' in request.GET):
        ticker_query = request.GET['q'].strip()
        search = True
    if ('q' in request.GET)\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper()).exists()\
            and SecurityPriceHist.objects\
            .filter(ticker_sym=request.GET['q'].strip().upper())[0]\
            .issuer is not None:
        found_ticker = request.GET['q'].strip().upper()
        found_sph = SecurityPriceHist.objects\
            .filter(ticker_sym=found_ticker)[0]
        # Note that the issuer could be None if the sph hasn't been linked.
        issuer = found_sph.issuer
        signals = Signal.objects.filter(issuer=issuer)
        if signals.exists():
            last_signal_sent = signals.latest('signal_date').signal_date
        else:
            last_signal_sent = None
        if issuer is None:
            messagetext = \
                'Ticker could not be added! Contact customer support for help.'
            messages.info(request, messagetext)
            found_sph = None
        elif WatchedName.objects.filter(user=request.user)\
                .filter(issuer=issuer)\
                .filter(securitypricehist=found_sph).exists():
            already_exists = True
        else:
            WatchedName(user=request.user,
                        issuer=issuer,
                        securitypricehist=found_sph,
                        ticker_sym=found_sph.ticker_sym,
                        last_signal_sent=last_signal_sent).save()
    return render_to_response('managewatchlist.html',
                              {'username': request.user.username,
                               'already_exists': already_exists,
                               'found_ticker': found_ticker,
                               'search': search,
                               'ticker_query': ticker_query,
                               'watchlist': watchlist,
                               },
                              context_instance=RequestContext(request),
                              )


@login_required()
def pwreset(request):
    subject = 'Temporary [PRODUCT NAME] Password'
    new_pw = User.objects.make_random_password()

    message =\
        'We received your password reset request for [PRODUCT NAME].\n\n'\
        + 'Your new password is %s and we suggest that you reset this to '\
        % new_pw\
        + 'something easier to remember. If you did not request a '\
        + 'password reset, please contact us at [SUPPORT EMAIL ADDRESS].\n\n'\
        + 'If you have any questions, feel free to reply to this email.\n\n'\
        + 'Regards,\n'\
        + '[COMPANY NAME] Support'
    from_email = settings.EMAIL_HOST_USER
    # request.user.email
    to_list = [request.user.email]

    u = User.objects.get(username__exact=request.user.username)
    u.set_password(new_pw)
    u.save()
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    print message
    request.user.email

    messagetext = \
        'You should receive a new temporary password shortly.'
    messages.warning(request, messagetext)
    return HttpResponseRedirect('/changepw/')


@login_required()
def changepwauth(request):
    username = request.user.username
    password = request.POST.get('oldpassword', '')
    newpassword = request.POST.get('newpassword', '')
    confirmnewpassword = request.POST.get('confirmnewpassword', '')
    userauth = auth.authenticate(username=username, password=password)
    if userauth is not None and newpassword == confirmnewpassword:
        user = \
            User.objects.get(username=username)
        user.set_password(newpassword)
        user.save()
        messagetext = \
            'New Password Saved'
        messages.success(request, messagetext)
        return HttpResponseRedirect('/accountinfo/')
    if userauth is None:
        messagetext = \
            'Incorrect Password Entered'
        messages.warning(request, messagetext)
        return HttpResponseRedirect('/changepw/')

    if newpassword != confirmnewpassword:
        messagetext = \
            'The new and confirmed blanks do not match'
        messages.warning(request, messagetext)
        return HttpResponseRedirect('/changepw/')
