FROM midebian

RUN useradd -ms /bin/bash dev

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]
