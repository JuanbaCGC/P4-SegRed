FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install flask flask-restful flask-limiter requests

COPY entrypoint.sh /entrypoint.sh
COPY apiAuth.py /apiAuth.py
COPY http_status_codes.py /http_status_codes.py
COPY tokens.json /tokens.json
COPY users.json /users.json

COPY authcert.pem /authcert.pem
COPY authkey.pem /authkey.pem

COPY filescert.pem /filescert.pem
COPY filescert.pem /usr/local/share/ca-certificates/dockerFiles.crt

RUN update-ca-certificates

ENTRYPOINT /entrypoint.sh
