[![Foodgram_workflow](https://github.com/vardeath/foodgram-project/actions/workflows/foodgram_workflow.yaml/badge.svg)](https://github.com/vardeath/foodgram-project/actions/workflows/foodgram_workflow.yaml)

# Foodgram-project
http:/178.154.247.254
## Описание
Приложение «Продуктовый помощник»: сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект был выполнен в качестве дипломного задания в Яндекс Практикум.
## Стек технологий
- Python
- Django
- PostgreSQL
- Docker
- Nginx
- Gunicorn
- Git / GitHub actions

## Как запустить проект, используя Docker (база данных PostgreSQL):
1) Клонируйте репозиторий с проектом:
```
git clone https://github.com/netshy/foodgram-project.git
```
2) В директории проекта создайте файл .env, по пути `<project_name>/.env`, в котором пропишите следующие переменные окружения:
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=postgres 
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
- DB_HOST=db 
- DB_PORT=5432
- SECRET_KEY=<your secret key>

##### Для локального использования DB_HOST=127.0.0.1
##### Для включения дебага DEBUG=True

3) С помощью Dockerfile и docker-compose.yaml разверните проект:

- `sudo docker-compose up -d`
- `docker-compose run --rm web python manage.py migrate`
- `docker-compose run --rm web python manage.py collectstatic --no-input`
- Загрузка бд тестовыми данными:
- `docker-compose run --rm web python manage.py shell`
- `>>> from django.contrib.contenttypes.models import ContentType`
- `>>> ContentType.objects.all().delete()`
- `>>> quit()`
- затем:
- `docker-compose run --rm web python manage.py loaddata dump.json`

