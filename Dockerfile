FROM python:3.11-alpine

WORKDIR /usr/app

COPY requirements.txt  /usr/app/

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "src/server.py" ]



