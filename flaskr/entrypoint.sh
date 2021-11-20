#!/bin/bash

exec gunicorn --config gunicorn.conf.py app:app

