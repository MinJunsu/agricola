#!/bin/sh
. .venv/bin/activate && daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
