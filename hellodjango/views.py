from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf


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
