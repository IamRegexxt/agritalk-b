#!/bin/bash

# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade

echo "Migrations completed successfully."