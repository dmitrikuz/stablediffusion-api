FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


COPY requirements.txt /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY ./ /app


ENV APP_MODULE sdapp.app:app
