FROM python:alpine

WORKDIR /usr/src/app

EXPOSE 8000

RUN apk add --no-cache postgresql-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD runserver.sh
