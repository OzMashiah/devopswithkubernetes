#!/bin/bash

# Set the backup filename (current date/time)
BACKUP_FILE="/tmp/backup_$(date +'%Y%m%d%H%M').sql.gz"

# Dump the PostgreSQL database and compress the output
pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE | gzip > $BACKUP_FILE

# Upload the backup to Google Cloud Storage
gsutil cp $BACKUP_FILE gs://your-backup-bucket/

# Clean up the backup file
rm $BACKUP_FILE
