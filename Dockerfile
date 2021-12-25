FROM python:3.9

# update pip
RUN python -m pip install --upgrade pip

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD cryptography_bot/main.py /

CMD [ "python3", "-u", "/main.py" ]
