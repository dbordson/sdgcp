from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
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
        return HttpResponseRedirect('/sdapp/')
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
