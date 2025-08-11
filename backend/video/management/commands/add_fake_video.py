import logging
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from video.models import Video
from users.models import User
from core.constants import MAX_LENGTH_VIDEO_NAME

logger = logging.getLogger('models')


class Command(BaseCommand):
    help = 'Создает указанное количество видео с фейковыми данными'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100000, help='Количество создаваемых видео')

    def handle(self, *args, **options):
        count = options['count']
        if count <= 0:
            self.stderr.write(self.style.ERROR('Количество видео должно быть положительным'))
            return

        fake = Faker()

        # Загружаем всех существующих пользователей
        self.stdout.write('Загрузка существующих пользователей...')
        existing_users = list(User.objects.all())
        if not existing_users:
            self.stderr.write(self.style.ERROR('Нет пользователей в базе данных. Создайте пользователей сначала.'))
            return

        videos = []
        self.stdout.write(f'Генерация {count} видео...')
        try:
            for i in range(count):
                owner = random.choice(existing_users)
                is_published = random.choice([True, False])
                name = fake.sentence(nb_words=5)[:MAX_LENGTH_VIDEO_NAME]
                total_likes = random.randint(0, 1000)

                video = Video(
                    owner=owner,
                    is_published=is_published,
                    name=name,
                    total_likes=total_likes,
                )
                videos.append(video)

                # Вывод прогресса каждые 1000 видео
                if (i + 1) % 1000 == 0:
                    self.stdout.write(f'Сгенерировано {i + 1} видео...')

            with transaction.atomic():
                Video.objects.bulk_create(videos, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f'Успешно создано {len(videos)} видео'))
            logger.info(f'Успешно создано {len(videos)} видео')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при создании видео: {str(e)}'))
            logger.error(f'Ошибка при создании видео: {str(e)}')