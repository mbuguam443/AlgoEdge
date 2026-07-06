#!/usr/bin/env bash
# AlgoEdge cPanel Deployment Script
# Run from SSH Terminal or cPanel Terminal
set -o errexit

echo "=== AlgoEdge cPanel Deployment ==="

# === CONFIGURATION - UPDATE THESE ===
REPO_DIR="$HOME/repo"
VENV_DIR="$HOME/virtualenv"
DOMAIN="yourdomain.com"

echo "[1/5] Pulling latest code..."
cd "$REPO_DIR"
git pull origin master

echo "[2/5] Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3.12 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$REPO_DIR/requirements.txt"

echo "[3/5] Setting up .env..."
if [ ! -f "$REPO_DIR/.env" ]; then
    cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"
    echo ">>> Edit $REPO_DIR/.env with your settings before continuing"
    echo "    DJANGO_SECRET_KEY=<generate a key>"
    echo "    DJANGO_DEBUG=False"
    echo "    DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN"
    echo "    SITE_URL=https://$DOMAIN"
    echo "    DJANGO_SECURE_SSL=True"
    exit 1
fi

# Load env vars from .env
export $(grep -v '^#' "$REPO_DIR/.env" | xargs)

echo "[4/5] Running migrations & collecting static..."
cd "$REPO_DIR"
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

echo "[5/5] Setting permissions..."
find "$REPO_DIR" -type d -exec chmod 755 {} \;
find "$REPO_DIR" -type f -exec chmod 644 {} \;
chmod 755 "$REPO_DIR/passenger_wsgi.py"
chmod 644 "$REPO_DIR/db.sqlite3" 2>/dev/null || true

# Restart Passenger
touch "$REPO_DIR/tmp/restart.txt" 2>/dev/null || true
mkdir -p "$REPO_DIR/tmp"

echo "=== Deployment complete! ==="
echo "Visit: https://$DOMAIN"
