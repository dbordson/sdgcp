"""
WSGI config for hellodjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(os.path.abspath(os.path.join(cwd, os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellodjango.settings")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())