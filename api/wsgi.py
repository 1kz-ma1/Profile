"""
WSGI config for Vercel deployment.

Exposes the WSGI callable as a module-level variable named ``app``
so that Vercel Python runtime can detect and serve the Django app.
"""

import os
from django.core.wsgi import get_wsgi_application

# Point to the existing Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workpro.settings")

# Vercel expects a variable named `app` for WSGI
app = get_wsgi_application()
