FROM python:3.8-slim-buster
# ENV NODE_ENV development
# Add a work directory
WORKDIR /twitter-scraping-backend
# Cache and Install dependencies
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install -y git
RUN pip3 install -r requirements.txt
COPY . .