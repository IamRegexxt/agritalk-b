#!/bin/bash

# Run Celery worker
 celery -A app.services.celery_service.celery worker --pool=solo --loglevel=info