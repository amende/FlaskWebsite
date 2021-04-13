FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install setuptools --upgrade

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY .env.template .env

RUN key=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

RUN sed -i "s/pleasereplacebyrandomshit/${key}/" .env

COPY . /app

ENTRYPOINT [ "python3" ]

CMD ["main.py"]

