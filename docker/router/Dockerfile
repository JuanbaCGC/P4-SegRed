FROM midebian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    make \
    python3-pip

RUN pip install requests

COPY entrypoint.sh /entrypoint.sh
COPY test.py /test.py
ENTRYPOINT ["bash","entrypoint.sh"]
