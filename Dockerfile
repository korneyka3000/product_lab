FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY start.sh /start
RUN chmod +x /start

COPY . .

