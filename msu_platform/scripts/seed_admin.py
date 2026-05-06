import os
import sys
from pathlib import Path

# Add project root to sys.path so 'apps' and 'config' can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import django

def seed():
    try:
        # Set settings module
        if not os.environ.get('DJANGO_SETTINGS_MODULE'):
            os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
            
        django.setup()
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        email = os.environ.get('ADMIN_EMAIL', 'admin@msu.ac.zw')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        first_name = os.environ.get('ADMIN_FIRST_NAME', 'Admin')
        last_name = os.environ.get('ADMIN_LAST_NAME', 'User')
        
        if User.objects.filter(email=email).exists():
            print(f"SEED_EXISTS: {email}")
            return True
            
        print(f"Creating admin user: {email}...")
        User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            student_id='MSU000000',
            faculty='science',
            department='IT',
            year_of_study=4,
            is_verified=True
        )
        print("SEED_SUCCESS")
        return True
    except Exception as e:
        print(f"SEED_ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if seed():
        sys.exit(0)
    else:
        sys.exit(1)
