#!/usr/bin/env bash
# AlgoEdge cPanel Deployment Script
# Run from SSH Terminal or cPanel Terminal
set -o errexit

echo "=== AlgoEdge cPanel Deployment ==="
echo "Target: https://algoedge.greatjourns.com"

# === CONFIGURATION - UPDATE THESE ===
REPO_DIR="$HOME/algoedge"
VENV_DIR="$HOME/virtualenv/algoedge"
DOMAIN="algoedge.greatjourns.com"

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
    cat > "$REPO_DIR/.env" << 'ENVEOF'
# Django
DJANGO_SECRET_KEY=<GENERATE_A_SECRET_KEY>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=algoedge.greatjourns.com
CSRF_TRUSTED_ORIGINS=https://algoedge.greatjourns.com
SITE_URL=https://algoedge.greatjourns.com
DJANGO_SECURE_SSL=True

# MySQL Database (cPanel)
DB_NAME=greatjou_algoedge
DB_USER=greatjou_algoedge
DB_PASSWORD=Me32323383#&
DB_HOST=localhost
DB_PORT=3306

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@algoedge.com

# Payments (optional)
STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=
PAYPAL_CLIENT_ID=

# M-Pesa (optional)
MPESA_CONSUMER_KEY=
MPESA_CONSUMER_SECRET=

# Links
BROKER_AFFILIATE_LINK=
DISCORD_INVITE_LINK=
TELEGRAM_INVITE_LINK=
ENVEOF
    echo ">>> .env created. Edit $REPO_DIR/.env to add DJANGO_SECRET_KEY and any API keys."
    echo "    Generate a secret key at: https://djecrety.ir/"
    exit 1
fi

# Load env vars from .env
set -a; source "$REPO_DIR/.env"; set +a

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
mkdir -p "$REPO_DIR/tmp"
touch "$REPO_DIR/tmp/restart.txt"

echo "=== Deployment complete! ==="
echo "Visit: https://$DOMAIN"
