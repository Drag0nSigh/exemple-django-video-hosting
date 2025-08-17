<h1>Описание проекта exemple_django_video_hosting</h1>

***

exemple_django_video_hosting это практическое задание по закрпелению Django. Это backend (api) сервиса по публикации видео с возможностью поставить лайки. Реализован минимальный функционал.

Ручки:
```
"/v1/videos/{video.id}/"
"/v1/videos/"
"/v1/videos/{video.id}/likes/"
"/v1/videos/ids/"
"/v1/videos/statistics-subquery/"
"/v1/videos/statistics-group-by/"
```

Автор: Drag0nsigh https://github.com/Drag0nSigh

Стек: Python 3.12, Django 5.2.5, Rest, Postgres

***

<h2>Установка</h2>

<h3>Локальное разворачивание с помощью Docker</h3>

Копирование репозитория

```
git clone https://github.com/Drag0nSigh/exemple-django-video-hosting.git
```

Переход в рабочую папку

```
cd backend
```

Создайте файл .env, пример как его заполнять в файле env_exemple

```
nano .env
```

Создание образов Docker из локального кода

```
docker compose -f docker_compose_all.yml build
```

Запуск контейнеров Docker

```
docker compose -f docker_compose_all.yml up
```

Миграция базы данных

Происходит при разворачивании проекта. Если надо убрать и перевести на ручную миграцию, уберите из docker_compose_all.yaml

```
"python manage.py makemigrations &&
 python manage.py migrate &&
 ```
И выполните миграцию в ручную

```
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py makemigrations
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py migrate
```

Сбор статики, так же реализован при сборке, если вы хотите делать это в ручную, то надо убрать из уберите из docker_compose_all.yaml

```
python manage.py collectstatic --noinput &&
```



```
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py collectstatic --noinput
```

Создание супер пользователя

```
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py createsuperuser
```

Загрузка тестовых данных (если требуется)

```
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py add_fake_users
docker compose -f docker_compose_all.yml exec backend-exemple_video_hosting python manage.py add_fake_video
```


