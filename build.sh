#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Auto-create superuser from environment variables
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'salon')
password = os.environ.get('ADMIN_PASSWORD', 'admin1234')
email    = os.environ.get('ADMIN_EMAIL', 'admin@salon.com')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser "{username}" created.')
else:
    print(f'Superuser "{username}" already exists.')
EOF
