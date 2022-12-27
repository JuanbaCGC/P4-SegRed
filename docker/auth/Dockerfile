FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install flask flask-restful flask-limiter requests

COPY entrypoint.sh /entrypoint.sh
COPY apiAuth.py /home/api/apiAuth.py
COPY http_status_codes.py /home/api/http_status_codes.py
COPY tokens.json /home/api/tokens.json
COPY users.json /home/api/users.json

ENTRYPOINT /entrypoint.sh
