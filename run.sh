#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Perform database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run the Flask app using Gunicorn
gunicorn -b 0.0.0.0:8000 -w 4 app:app

