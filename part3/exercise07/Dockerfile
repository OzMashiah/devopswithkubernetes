FROM google/cloud-sdk:slim

RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    gzip \
    && rm -rf /var/lib/apt/lists/*

COPY backup.sh /usr/local/bin/backup.sh

RUN chmod +x /usr/local/bin/backup.sh

CMD ["/usr/local/bin/backup.sh"]

