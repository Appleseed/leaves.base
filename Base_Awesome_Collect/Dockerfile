FROM python:3.6
WORKDIR /Base_Awesome_Collect
ADD . /Base_Awesome_Collect
RUN python3.6 -m pip install redis \
    && python3.6 -m pip install sqlalchemy \
    && python3.6 -m pip install watson-developer-cloud \
    && python3.6 -m pip install aiohttp \
    && python3.6 -m pip install wallabag_api \
    && python3.6 -m pip install requests 
CMD [ "python3.6", "Subscribe.py" ]