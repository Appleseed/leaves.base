FROM python:3.6

# Install prerequisites
RUN python3.6 -m pip install cassandra-driver \
	&& python3.6 -m pip install flask 

WORKDIR /leaves.api.query
ADD . /leaves.api.query

CMD ["python", "App.py"]
