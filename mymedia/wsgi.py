"""
WSGI config for mymedia project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mymedia.settings')

application = get_wsgi_application()
