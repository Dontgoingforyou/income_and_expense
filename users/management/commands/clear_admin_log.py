from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_admin_log")
        self.stdout.write(self.style.SUCCESS('Successfully cleared admin log entries'))