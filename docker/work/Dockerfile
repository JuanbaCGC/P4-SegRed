FROM midebian

RUN useradd -ms /bin/bash dev
RUN chown dev:dev -R /home/dev
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]
