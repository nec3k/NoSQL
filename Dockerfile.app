FROM python:3.10-alpine
WORKDIR /Project1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /Project1
RUN pip install -r requirements.txt --no-cache-dir
COPY ./Project1 /Project1
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000