FROM python:3.6
WORKDIR /redis_pub
ADD . /redis_pub
RUN python3.6 -m pip install watchdog \
    && python3.6 -m pip install redis
CMD [ "python3.6", "eventFileCreate.py" ]