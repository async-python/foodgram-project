FROM python:3.9-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PROD True
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000