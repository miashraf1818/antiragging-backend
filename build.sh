cat > build.sh << 'EOF'
#!/usr/bin/env bash
set -o errexit

echo "==> Upgrading pip..."
python -m pip install --upgrade pip

echo "==> Installing from requirements.txt..."
python -m pip install -r requirements.txt

echo "==> Verifying gunicorn installation..."
python -m pip show gunicorn

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "==> Running migrations..."
python manage.py migrate

echo "==> Build complete!"
EOF
