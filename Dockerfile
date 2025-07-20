FROM python:3.13-alpine

RUN pip install --upgrade pip
RUN apk add --no-cache bash postgresql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh", "./entrypoint.sh"]