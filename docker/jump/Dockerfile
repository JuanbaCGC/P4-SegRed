FROM midebian

RUN useradd -ms /bin/false jump && \
    mkdir /home/jump/.ssh && \
    chmod 700 /home/jump/.ssh
COPY authorized_keys /home/jump/.ssh/authorized_keys
COPY authorized_keys /home/jump/.ssh/authorized_keys.dev
COPY authorized_keys /home/jump/.ssh/authorized_keys.dev.pub
COPY authorized_keys /home/jump/.ssh/authorized_keys.op.pub
COPY authorized_keys /home/jump/.ssh/authorized_keys.op
RUN chown jump:jump -R /home/jump

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
