import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'algoedge.settings'
django.setup()

from django.core.management import call_command

print("=== AlgoEdge Deploy ===")

print("[1/3] Running migrations...")
call_command('migrate', '--noinput')

print("[2/3] Collecting static files...")
call_command('collectstatic', '--noinput', '--clear')

print("[3/3] Restarting Passenger...")
os.makedirs('tmp', exist_ok=True)
open('tmp/restart.txt', 'a').close()

print("=== Deploy complete! ===")
