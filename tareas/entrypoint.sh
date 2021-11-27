#!/bin/bash

exec celery -A tareas worker -l info 

