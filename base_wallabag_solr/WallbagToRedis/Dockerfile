FROM python:3.6
WORKDIR /redis_sub
ADD . /redis_sub
RUN python3.6 -m pip install cassandra-driver \
    && python3.6 -m pip install redis \
    && python3.6 -m pip install aiohttp \
    && python3.6 -m pip install wallabag_api \
    && python3.6 -m pip install requests 
CMD [ "python3.6", "IndexAllWallabagDoc.py" ]