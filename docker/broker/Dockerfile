FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install flask flask-restful flask-limiter requests

COPY entrypoint.sh /entrypoint.sh
COPY apiBroker.py /home/api/apiBroker.py
COPY http_status_codes.py /home/api/http_status_codes.py

ENTRYPOINT /entrypoint.sh