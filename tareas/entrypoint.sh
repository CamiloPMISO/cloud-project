#!/bin/bash

exec celery -A tareas worker -l info -Q process_audio

