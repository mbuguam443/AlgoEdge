#!/usr/bin/env bash
set -o errexit

echo "=== AlgoEdge Deploy Script ==="
echo "Target: https://algoedge.greatjourns.com"

# Activate virtual environment (adjust path if needed)
VENV_DIR="$HOME/virtualenv/algoedge"
# cPanel sometimes puts version in path; try both
if [ -d "$VENV_DIR/3.12/bin" ]; then
    source "$VENV_DIR/3.12/bin/activate"
elif [ -d "$VENV_DIR/bin" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "Could not find virtualenv at $VENV_DIR"
    exit 1
fi

echo "Virtualenv activated"

# Migrate database
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Restart Passenger
mkdir -p tmp
touch tmp/restart.txt

echo "=== Done! ==="