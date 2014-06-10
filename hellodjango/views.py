from django.shortcuts import render_to_response
# confirm listening
# Hardcoded link


def home(request):
    return render_to_response('hellodjango/home.html')
