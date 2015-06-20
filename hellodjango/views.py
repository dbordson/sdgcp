from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail


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
def pwreminder(request):
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
