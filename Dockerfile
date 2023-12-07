FROM python:3.10.12-slim AS dependencies
ENV TZ="America/Sao_Paulo"
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN apt-get -y install python3-pip git gcc libpq-dev perl libjson-perl

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["flask", "run", "--host", "0.0.0.0", "--port=5005"] #local development

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"] 