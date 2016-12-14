"""
WSGI config for PJT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from server.customLogging import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PJT.settings")

print("ici")
initializeLog("PJT", "PJT.txt", True, 10)
LOGINFO("LOG INITIALIZED in wsgi")

application = get_wsgi_application()
