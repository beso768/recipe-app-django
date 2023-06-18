"""Django command to watch for database connection"""
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to watch for database connection"""

    def handle(self, *args, **options):
        self.stdout.write("Waitingfor database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable , waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
