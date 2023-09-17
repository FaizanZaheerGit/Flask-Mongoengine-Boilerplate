FROM python:3.10.11-alpine

WORKDIR /Flask-Mongoengine-Boilerplate

COPY . /Flask-Mongoengine-Boilerplate

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
