FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install flask flask-restful requests

COPY entrypoint.sh /entrypoint.sh
COPY apiFile.py /apiFile.py
COPY http_status_codes.py /http_status_codes.py

ENTRYPOINT ["bash", "entrypoint.sh"]
