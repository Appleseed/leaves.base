FROM ubuntu:16.04
MAINTAINER niro;

# Install prerequisites
RUN apt-get -qq update \
&& apt-get -qq -y install curl \
&& apt-get install -y software-properties-common \
&& add-apt-repository ppa:jonathonf/python-3.6 \
&& apt-get update \
&& apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6 \
&& apt-get -y install zsh \
&& apt-get -y install git-core \
&& python3.6 -m pip install pip --upgrade \
&& python3.6 -m pip install wheel \
&& python3.6 -m pip install flask \
&& python3.6 -m pip install markdown-to-json \
&& python3.6 -m pip install wallabag_api \
&& python3.6 -m pip install redis

# Set the working directory to /app
WORKDIR /awesome_transform

# Copy the current directory contents into the container at /app
ADD ../ /awesome_transform

CMD ["python3.6", "App.py"]

