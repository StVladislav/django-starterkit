"""
This script need for init super user
when project run as a docker container
"""

import os
import django


def main():
    # THIS SHOULD BE SET BEFORE django.setup
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    from src.authentication.models import User

    email = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin@myemail.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', '123')
    first_name = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')

    user = User.objects.filter(email=email).first()

    if user:
        return
    
    User.objects.create_superuser(
        email=email,
        first_name=first_name,
        password=password
    )


if __name__ == "__main__":
    main()