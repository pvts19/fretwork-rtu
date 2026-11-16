"""Перенос данных из базы ПР7 (data/restspot.sqlite) в модели Django.

Запуск:  python manage.py import_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from db.database import DB_PATH, get_connection
from places.models import Place
from users.models import User
from visits.models import Visit


class Command(BaseCommand):
    help = 'Переносит места, пользователей и посещения из SQLite ПР7'

    @transaction.atomic
    def handle(self, *args, **options):
        if not DB_PATH.exists():
            self.stderr.write('Нет базы ПР7: python -m db.import_json')
            return
        with get_connection() as conn:
            places = conn.execute('SELECT * FROM places').fetchall()
            users = conn.execute('SELECT * FROM users').fetchall()
            visits = conn.execute('SELECT * FROM visits').fetchall()
        # id сохраняются, поэтому связи переносятся без потерь
        for row in places:
            Place.objects.update_or_create(id=row['id'], defaults={
                k: row[k] for k in row.keys() if k != 'id'})
        for row in users:
            User.objects.update_or_create(id=row['id'], defaults={
                'name': row['name'], 'email': row['email']})
        for row in visits:
            Visit.objects.update_or_create(id=row['id'], defaults={
                'place_id': row['place_id'], 'user_id': row['user_id'],
                'date': row['date'], 'people': row['people'],
                'status': row['status'], 'rating': row['rating']})
        self.stdout.write(self.style.SUCCESS(
            f'Перенесено: мест {len(places)}, пользователей {len(users)}, '
            f'посещений {len(visits)}'))
