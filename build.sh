cat > build.sh << 'EOF'
#!/usr/bin/env bash
set -o errexit

echo "==> Activating virtual environment..."
source /opt/render/project/src/.venv/bin/activate || true

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing from requirements.txt..."
pip install -r requirements.txt

echo "==> Verifying gunicorn installation..."
which gunicorn
gunicorn --version

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "==> Running migrations..."
python manage.py migrate

echo "==> Build complete!"
EOF
