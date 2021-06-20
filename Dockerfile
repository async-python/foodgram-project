FROM python:3.8-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --no-input
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000