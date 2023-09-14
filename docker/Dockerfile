FROM python:3.10.0-slim-buster

WORKDIR /application

RUN pip install flask Flask-SQLAlchemy Flask-Login Jinja2

CMD flask run --host=0.0.0.0 --port=8082