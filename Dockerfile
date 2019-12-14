FROM python:3.8-alpine

EXPOSE 8080

WORKDIR /app/src

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "feedodon2.wsgi:application", "--bind", "0.0.0.0:8080", "--log-file", "-", "--access-logfile", "-"]