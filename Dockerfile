FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}
CMD ["gunicorn", "prod_django_project_aws.wsgi:application", "--bind", "0.0.0.0:8000"]
