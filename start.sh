#!/bin/sh
. .venv/bin/activate
python3 main.py
daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
