#!/bin/bash

echo "======================================"
echo "MSU Platform - Quick Start Setup"
echo "======================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if migrations exist
if [ ! -d "apps/users/migrations" ]; then
    echo "Creating migrations..."
    python manage.py makemigrations
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Seed permissions
echo "Seeding permissions and roles..."
python manage.py seed_permissions

# Check if superuser exists
echo ""
echo "======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Run server: python manage.py runserver"
echo "3. Visit admin: http://localhost:8000/admin/"
echo ""
