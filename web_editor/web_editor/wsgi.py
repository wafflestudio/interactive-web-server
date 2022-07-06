"""
WSGI config for web_editor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import settings

from django.core.wsgi import get_wsgi_application

import socketio
import eventlet
import eventlet.wsgi


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_editor.settings')

django_app = get_wsgi_application() # application
sio = socketio.Server(async_mode='eventlet', cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS, cors_credentials=True)
# check validity of cors_allowed_origins = ... code
application = socketio.WSGIApp(sio, django_app)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
