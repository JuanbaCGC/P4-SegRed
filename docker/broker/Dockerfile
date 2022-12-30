FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip 

RUN pip install flask flask-restful flask-limiter requests

COPY entrypoint.sh /entrypoint.sh
COPY apiBroker.py /apiBroker.py
COPY http_status_codes.py /http_status_codes.py

COPY brokercert.pem /brokercert.pem
COPY brokerkey.pem /brokerkey.pem

COPY authcert.pem /authcert.pem
COPY filescert.pem /filescert.pem
COPY authcert.pem /usr/local/share/ca-certificates/dockerAuth.crt
COPY filescert.pem /usr/local/share/ca-certificates/dockerFiles.crt

RUN update-ca-certificates

ENTRYPOINT /entrypoint.sh