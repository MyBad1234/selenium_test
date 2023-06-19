FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3

WORKDIR /app
COPY . .

CMD ["python3", "test.py"]