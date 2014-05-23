#!/bin/sh
export DJANGO_SETTINGS_MODULE=climata_viewer.settings
celery -A climata_viewer worker -l info >> ../logs/celery.log 2>> ../logs/celery-error.log
