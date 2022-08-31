FROM python:3.9.13-buster

LABEL maintainer="praveen.androids@gmail.com"

WORKDIR /app

COPY . /app

RUN pip install flask 

ENV FLASK_ENV=development 

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

