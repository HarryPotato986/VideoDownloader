#!/bin/bash

echo "Starting cron daemon..."
service cron start

echo "Starting Gunicorn..."
gunicorn -w 4 -b 0.0.0.0 --forwarded-allow-ips='*' wsgi:app