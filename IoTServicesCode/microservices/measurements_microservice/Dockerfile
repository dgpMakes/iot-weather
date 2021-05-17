FROM python:3.7.3

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

RUN pip install urllib3 mysql-connector-python Flask Flask-Cors PyYAML

CMD ["python", "-u", "measurements_manager_api.py"]