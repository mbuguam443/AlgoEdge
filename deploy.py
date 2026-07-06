import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'algoedge.settings'

django.setup()

from django.core.management import call_command

print("=== AlgoEdge Deploy ===")

print("[1/3] Running migrations...")
call_command('migrate', '--noinput')

print("[2/3] Collecting static files...")
static_dir = os.path.join(BASE_DIR, 'static_assets')
os.makedirs(static_dir, exist_ok=True)
call_command('collectstatic', '--noinput')

print("[3/3] Restarting Passenger...")
os.makedirs('tmp', exist_ok=True)
open('tmp/restart.txt', 'a').close()

print("=== Deploy complete! ===")
