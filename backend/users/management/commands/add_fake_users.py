import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from users.models import User
from core.constants import MAX_LENGTH_USERS_CHAR, MAX_LENGTH_EMAIL

logger = logging.getLogger('models')


class Command(BaseCommand):
    help = 'Создает указанное количество пользователей с фейковыми данными'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10000, help='Количество создаваемых пользователей')

    def handle(self, *args, **options):
        count = options['count']
        if count <= 0:
            self.stderr.write(self.style.ERROR('Количество пользователей должно быть положительным'))
            return

        fake = Faker()
        existing_users = User.objects.values('username', 'email')
        used_usernames = {user['username'] for user in existing_users}
        used_emails = {user['email'] for user in existing_users}
        users = []

        self.stdout.write(f'Генерация {count} пользователей...')
        try:
            for _ in range(count):
                while True:
                    email = fake.email()
                    if len(email) <= MAX_LENGTH_EMAIL and email not in used_emails:
                        used_emails.add(email)
                        break

                while True:
                    username = fake.user_name()
                    if len(username) <= MAX_LENGTH_USERS_CHAR and username not in used_usernames:
                        used_usernames.add(username)
                        break

                first_name = fake.first_name()[:MAX_LENGTH_USERS_CHAR]
                last_name = fake.last_name()[:MAX_LENGTH_USERS_CHAR]

                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                users.append(user)

            with transaction.atomic():
                User.objects.bulk_create(users, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f'Успешно создано {len(users)} пользователей'))
            logger.info(f'Успешно создано {len(users)} пользователей')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании пользователей: {str(e)}'))
            logger.error(f'Ошибка при создании пользователей: {str(e)}')
