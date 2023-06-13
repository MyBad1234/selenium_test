FROM python

ENV WEB_DB_NAME=clicker
ENV WEB_DB_USER=gena
ENV WEB_DB_PASSWORD=123456
ENV WEB_DB_HOST=db
ENV WEB_DB_PORT=5432

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "web.wsgi"]
