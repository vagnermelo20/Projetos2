"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``lication``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_lication

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

lication = get_asgi_lication()
