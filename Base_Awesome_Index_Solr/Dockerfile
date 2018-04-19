FROM python:3.6
WORKDIR /redis_solrPub
ADD . /redis_solrPub
RUN python3.6 -m pip install redis \
    && python3.6 -m pip install aiohttp \
    && python3.6 -m pip install requests \
	&& python3.6 -m pip install beautifulsoup4
CMD [ "python3.6", "process_solr.py" ]