#!/bin/bash

BACKUP_FILE="/tmp/backup_$(date +'%Y%m%d%H%M').sql.gz"

pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE | gzip > $BACKUP_FILE

gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
gsutil cp $BACKUP_FILE gs://devopswithkubernetes-backup-bucket/

rm $BACKUP_FILE
