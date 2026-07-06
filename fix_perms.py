import os
import stat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Fixing permissions...")
for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root:
        continue
    for d in dirs:
        path = os.path.join(root, d)
        try:
            os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except OSError as e:
            print(f"  Cannot chmod dir {path}: {e}")
    for f in files:
        path = os.path.join(root, f)
        try:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        except OSError as e:
            print(f"  Cannot chmod file {path}: {e}")

print("Done. Run 'python deploy.py' next.")
