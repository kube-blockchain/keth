FROM python:3.8 as lint
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install flake8 pylint
RUN flake8 *.py
RUN pylint *.py

FROM python:3.8 as build
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY templates ./templates
COPY *.py ./
EXPOSE 8080
CMD kopf run --liveness=http://0.0.0.0:8080/healthz handlers.py
