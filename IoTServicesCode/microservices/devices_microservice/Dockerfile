FROM python:3.7.3

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

RUN pip install mysql-connector-python Flask Flask-Cors PyYAML

ENTRYPOINT ["python"]
CMD ["devices_manager_api.py"]