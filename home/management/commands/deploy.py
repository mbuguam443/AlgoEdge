import os
import sys
import django
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run migration, collectstatic, and restart Passenger for cPanel/SSH deployment'

    def handle(self, *args, **options):
        self.stdout.write("=== AlgoEdge Deploy ===")

        self.stdout.write("[1/3] Running migrations...")
        call_command('migrate', '--noinput')

        self.stdout.write("[2/3] Collecting static files...")
        call_command('collectstatic', '--noinput', '--clear')

        self.stdout.write("[3/3] Restarting Passenger...")
        os.makedirs('tmp', exist_ok=True)
        open('tmp/restart.txt', 'a').close()

        self.stdout.write(self.style.SUCCESS("=== Deploy complete! ==="))
