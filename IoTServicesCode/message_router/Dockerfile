FROM python:3.7.3

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

RUN pip install requests paho-mqtt

CMD ["python", "-u", "message_router.py"]