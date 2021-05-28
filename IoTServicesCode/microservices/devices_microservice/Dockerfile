FROM python:3.7.3

RUN pip install mysql-connector-python Flask Flask-Cors PyYAML

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

CMD ["python", "-u", "devices_manager_api.py"]