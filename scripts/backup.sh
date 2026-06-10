#!/bin/bash

# Configuration
PROJECT_DIR="/app/worldCup"
BACKUP_DIR="$HOME/backups/worldcup"
ENV_FILE="$PROJECT_DIR/.env"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Get the database container name
CONTAINER_NAME=$(docker compose -f "$PROJECT_DIR/docker-compose.prod.yaml" ps -q db)

if [ -z "$CONTAINER_NAME" ]; then
    echo "Error: Database container not found."
    exit 1
fi

# Timestamp for the backup file
TIMESTAMP=$(date +"%Y%m%d_%H%M")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Execute pg_dump
echo "Starting backup of $POSTGRES_DB..."
docker exec -t "$CONTAINER_NAME" pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup successfully created: $BACKUP_FILE"
else
    echo "Error occurred during backup."
    exit 1
fi

# Rotation: Delete backups older than 7 days
echo "Cleaning up old backups..."
find "$BACKUP_DIR" -type f -name "backup_*.sql" -mtime +7 -delete

echo "Backup process completed."
