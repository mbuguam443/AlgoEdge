"""cPanel Passenger entry point."""
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algoedge.settings')

# Try loading .env from project root
env_file = os.path.join(PROJECT_DIR, '.env')
if os.path.isfile(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
