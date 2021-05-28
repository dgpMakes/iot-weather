FROM python:3.7.3

RUN pip install requests paho-mqtt

COPY /app /etc/usr/src
WORKDIR /etc/usr/src

CMD ["python", "-u", "message_router.py"]