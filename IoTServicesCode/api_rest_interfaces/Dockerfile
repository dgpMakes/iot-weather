FROM python:3.7.3

RUN pip install requests mysql-connector-python Flask Flask-Cors PyYAML

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

ENTRYPOINT ["python"]
CMD ["webapp_api.py"]