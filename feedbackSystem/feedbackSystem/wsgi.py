"""
WSGI config for feedbackSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedbackSystem.settings')

# Uncomment when deploying on Apache2
#sys.path.append('/path/to/project/feedbackSystem')
#sys.path.append('/path/to/project/feedbackSystem/feedbackSystem')

application = get_wsgi_application()

# Uncomment when deploying on Apache2
# from django.contrib.auth.handlers.modwsgi import check_password #, groups_for_user
# from django.core.handlers.wsgi import WSGIHandler

# application = WSGIHandler()