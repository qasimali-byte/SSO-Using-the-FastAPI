FROM python:3.10.8-slim-buster
# ENV NODE_ENV development
# Add a work directory
WORKDIR /SSO_IDP
# Cache and Install dependencies
COPY requirements.txt requirements.txt
RUN apt update
RUN apt-get install -y build-essential
RUN apt-get install -y python3-psycopg2
# RUN apt-get install -y python3-pip
RUN apt install -y postgresql postgresql-contrib 
RUN apt install -y python3-dev libpq-dev
RUN apt install -y git
RUN pip3 install -r requirements.txt
COPY . .