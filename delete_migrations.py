"""
Use this for remove all migrations file
from a project. 

>>> python ./delete_migrations.py
"""

import os
import glob


def delete_migration_files():
    migrations_pattern = os.path.join("src", '*', 'migrations', '*.py')
    migration_files = glob.glob(migrations_pattern)
    migration_cache_pattern = os.path.join("src", '*', 'migrations', '__pycache__')
    migration_cache_dirs = glob.glob(migration_cache_pattern)

    for migration_file in migration_files:
        if not migration_file.endswith('__init__.py'):
            try:
                os.remove(migration_file)
            except OSError as e:
                print(f'Error deleting file {migration_file}: {e}')

    for cache_dir in migration_cache_dirs:
        try:
            os.remove(cache_dir)
        except OSError as e:
            print(f'Error deleting file {cache_dir}: {e}')


if __name__ == "__main__":
    delete_migration_files()
