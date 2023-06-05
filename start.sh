#!/bin/sh
. .venv/bin/activate
<<<<<<< Updated upstream
python3 main.py
=======
>>>>>>> Stashed changes
daphne -b 0.0.0.0 -p 8000 agricola.asgi:application
