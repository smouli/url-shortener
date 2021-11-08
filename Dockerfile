FROM python:3.8.2-alpine
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
CMD python server.py
