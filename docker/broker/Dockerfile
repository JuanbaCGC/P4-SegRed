FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install flask flask-restful flask-limiter

COPY entrypoint.sh /entrypoint.sh
COPY /api /home/api

ENTRYPOINT /entrypoint.sh