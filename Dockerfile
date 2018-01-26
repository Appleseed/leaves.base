FROM ubuntu:16.04
MAINTAINER niro;

# Install prerequisites
RUN apt-get -qq update && apt-get -qq -y install curl \
&& apt-get -y install zsh && apt-get -y install git-core


# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /awesome_transform

# Copy the current directory contents into the container at /app
ADD awesome-transform /awesome_transform

# Install any needed packages specified in requirements.txt
RUN pip install markdown-to-json

COPY awesome-transform/md_to_json /usr/local/bin/md_to_json

ENTRYPOINT ["python", "collect.awesome.md.csvpy.py"]
CMD ["https://raw.githubusercontent.com/Anant/awesome-sitecore/master/README.md","awesome_sitecore"]