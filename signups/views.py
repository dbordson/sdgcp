from django.shortcuts import (render_to_response, RequestContext,
                              HttpResponseRedirect)
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm

# def home(request):
#     return render_to_response('hellodjango/home.html')


def home(request):

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        # This automatically drops the signup into new credentials
        # this part should be removed if that shouldn't happen
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            return HttpResponseRedirect('/duplicate/')
        if User.objects.filter(username=form.cleaned_data['email']).exists():
            return HttpResponseRedirect('/duplicate/')
        user = \
            User.objects.create_user(username=form.cleaned_data['email'],
                                     email=form.cleaned_data['email'],
                                     first_name=form
                                     .cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'],
                                     password=form.cleaned_data['password'],
                                     )
        user.save()

        # From here on should stay in the view
        save_it = form.save(commit=False)
        save_it.save()
        messagetext = \
            'We will be in touch \n'\
            + '[for now the new user has been automatically given credentials]'
        messages.success(request, messagetext)
        return HttpResponseRedirect('/thank-you/')

    return render_to_response("signup.html",
                              locals(),
                              context_instance=RequestContext(request))


def thankyou(request):

    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request))


def duplicate_login(request):

    return render_to_response("duplicatelogin.html",
                              locals(),
                              context_instance=RequestContext(request))


def aboutus(request):

    return render_to_response("aboutus.html",
                              locals(),
                              context_instance=RequestContext(request))
