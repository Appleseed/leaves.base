FROM ubuntu:16.04
MAINTAINER niro;

RUN apt-get update
RUN apt-get install -y ffmpeg \
&& apt-get install -y libjpeg-dev \
&& apt-get install -y libpng-dev \
&& apt-get install -y libtiff-dev \
&& apt-get install -y libjasper-dev \
&& apt-get install -y libgtk2.0-dev \
&& apt-get install -y python-numpy \
&& apt-get install -y python-pycurl \
&& apt-get install -y webp \
&& apt-get install -y python-opencv \
&& apt-get install -y python-dev \
&& apt-get install -y python-pip 
RUN pip install thumbor

CMD ["thumbor"]
