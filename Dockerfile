FROM debian:buster
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential

WORKDIR /eBike

COPY ./ ./

RUN pip3 install --upgrade setuptools &&\
    pip3 install -r ./requirements.txt

ENTRYPOINT ["python3", "main.py"]
