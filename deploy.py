import os
import sys
import stat
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'algoedge.settings'

print("=== AlgoEdge Deploy ===")

print("[0/3] Fixing file permissions...")
for root, dirs, files in os.walk(BASE_DIR):
    for d in dirs:
        try:
            os.chmod(os.path.join(root, d), 0o755)
        except OSError:
            pass
    for f in files:
        try:
            os.chmod(os.path.join(root, f), 0o644)
        except OSError:
            pass

django.setup()

from django.core.management import call_command

print("[1/3] Running migrations...")
call_command('migrate', '--noinput')

print("[2/3] Collecting static files...")
static_root = os.path.join(BASE_DIR, 'staticfiles')
os.makedirs(static_root, exist_ok=True)
call_command('collectstatic', '--noinput', '--no-post-process')

print("[3/3] Restarting Passenger...")
os.makedirs('tmp', exist_ok=True)
open('tmp/restart.txt', 'a').close()

print("=== Deploy complete! ===")
