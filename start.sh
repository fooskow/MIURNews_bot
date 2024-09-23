#!/bin/bash

# Rimuovi la versione attuale di werkzeug e installa quella corretta
pip uninstall -y werkzeug
pip install werkzeug==2.0.3

# Avvia il bot
python3 bot_notizie.py
