# Introduction
Simple example on how to set up a PDF generation container using weasyprint ( https://weasyprint.org/ ), FLASK ( https://flask.palletsprojects.com/en/stable ) and gunicorn ( https://gunicorn.org/ ) 

# Notes
Set environmental variable SECRET_TOKEN to a kinda API key, the
endpoint will ensure that the request has Bearer SECRET_TOKEN as it's
Authorization header