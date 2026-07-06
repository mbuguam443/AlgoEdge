import os
import sys
import shutil
import tempfile
import zipfile
import urllib.request
import ssl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_URL = 'https://github.com/mbuguam443/AlgoEdge/archive/refs/heads/master.zip'

print("=== AlgoEdge Self-Update ===")

print("Downloading latest code from GitHub...")
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    zip_path = os.path.join(tempfile.gettempdir(), 'algoedge_update.zip')
    urllib.request.urlretrieve(ZIP_URL, zip_path, context=ctx)
except Exception:
    zip_path = os.path.join(tempfile.gettempdir(), 'algoedge_update.zip')
    urllib.request.urlretrieve(ZIP_URL, zip_path)

print("Extracting...")
extract_path = tempfile.mkdtemp()
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_path)
repo_root = os.path.join(extract_path, 'AlgoEdge-master')

print("Copying files (overwriting)...")
skip_files = {'.env', 'db.sqlite3', 'update.py', '.htaccess'}
for root, dirs, files in os.walk(repo_root):
    rel = os.path.relpath(root, repo_root)
    if rel == '.':
        rel = ''
    for f in files:
        if f in skip_files:
            continue
        src = os.path.join(root, f)
        dst = os.path.join(BASE_DIR, rel, f)
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        except PermissionError:
            print(f"  Skipped (permission): {rel}/{f}")
        except Exception as e:
            print(f"  Skipped ({e}): {rel}/{f}")

print("Cleaning up...")
os.remove(zip_path)
shutil.rmtree(extract_path, ignore_errors=True)

print("Running deploy steps...")
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'algoedge.settings'
import django
django.setup()
from django.core.management import call_command

print("[1/3] Running migrations...")
call_command('migrate', '--noinput')

print("[2/3] Collecting static files...")
static_dir = os.path.join(BASE_DIR, 'static_assets')
try:
    os.makedirs(static_dir, exist_ok=True)
except PermissionError:
    pass
call_command('collectstatic', '--noinput')

print("[3/3] Restarting Passenger...")
os.makedirs('tmp', exist_ok=True)
open('tmp/restart.txt', 'a').close()

print("=== Update complete! ===")
print("You may need to Restart the Python App from cPanel UI.")
