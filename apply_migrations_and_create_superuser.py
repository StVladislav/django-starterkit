"""
This script need for init super user
when project run as a docker container
"""

import os
import django
from django.db import connection
from django.core.management import call_command


"""
This file is using for init all migrations and
create superuser when database is initied.
"""


# THIS SHOULD BE SET BEFORE django.setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def create_pg_trgm_extension():
    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def main():
    from src.authentication.models import User

    create_pg_trgm_extension()
    call_command('migrate')

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
