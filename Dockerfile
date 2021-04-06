FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install setuptools --upgrade

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN pip3 freeze

COPY . /app

ENTRYPOINT [ "python3" ]

CMD ["main.py"]

