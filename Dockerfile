FROM ubuntu:16.04
MAINTAINER niro;

# Install prerequisites
RUN apt-get -qq update && apt-get -qq -y install curl \
&& apt-get -y install zsh && apt-get -y install git-core


# Use an official Python runtime as a parent image
#FROM python:2.7-slim
RUN apt-get -y install python python-pip

# Set the working directory to /app
WORKDIR /awesome_transform

# Copy the current directory contents into the container at /app
ADD . /awesome_transform

RUN chmod 777 /awesome_transform

# Install any needed packages specified in requirements.txt
RUN pip install markdown-to-json

#COPY md_to_json /usr/local/bin/md_to_json

RUN chmod 777 /usr/local/bin/

ENTRYPOINT ["python", "collect.awesome.md.csvpy.py"]
CMD ["https://raw.githubusercontent.com/Anant/awesome-sitecore/master/README.md","awesome_sitecore"]