#!/usr/bin/env bash
### python cache_purging.py
gunicorn --error-logfile err.log --access-logfile access.log -w2 --timeout 600 --graceful-timeout 600 -b 0.0.0.0:8080 -p svc.pid svc:app
