FROM python:3.11

WORKDIR /usr/src/app

COPY . .

CMD ["python", "-u", "main.py"]

