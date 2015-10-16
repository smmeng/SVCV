"""
WSGI config for pyMySQL project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

#There's an old mod_wsgi bug. 
#The current WSGI plugin for apache has a bug so we need to include the path in the environment. Uncomment the following before final deployment on Linux.
#import sys 
#sys.path.append('/var/www/html')
#sys.path.append('/var/www/html/pyMySQL')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyMySQL.settings")

application = get_wsgi_application()
