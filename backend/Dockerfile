FROM python:3.8

COPY wait-for-it.sh /usr/bin/wait-for-it
COPY docker_entrypoint.sh /docker_entrypoint.sh

RUN mkdir /app
WORKDIR /app

RUN apt update && \
    apt install -y postgresql-client

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD ["serve", "dev"]
