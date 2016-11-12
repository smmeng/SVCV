"""
WSGI config for airTraffic project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/usr/local/lib64/python2.7/site-packages/')
#sys.path.append('/usr/local/lib64/python2.7/site-packages/django')
#sys.path.append('/usr/local/lib64/python2.7/site-packages/django/core')
sys.path.append('/var/www')
sys.path.append('/var/www/html')
sys.path.append('/var/www/html/AirTraffic/')
sys.path.append('/var/www/html/AirTraffic/AirtrafficUI/')
sys.path.append('/var/www/html/AirTraffic/AirtrafficUI/static')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airTraffic.settings")

application = get_wsgi_application()
