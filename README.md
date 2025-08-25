# Introduction 

Simple example on how to set up a PDF generation container using weasyprint ( https://weasyprint.org/ ), FLASK ( https://flask.palletsprojects.com/en/stable ) and gunicorn ( https://gunicorn.org/ ) 

# Getting Started
pdfapi.py contains the actual service running over Flask. It uses weasyprint to generate the PDF. 
In front of the Fask server there is gunicorn acting as the WSGI Server.
By default the service listens port 5000

# Endpoints
The service has two endpoints:
## POST /request-token
Used to fetch JWT token that is used to access the actual PDF generation endpoint
application/json body content should be the followins:
```
{
	"api-key": "apikey",
	"application-id": "insomnia"
}
```
With a correct api-key the response is
```
{
    "token": "jwt token contents"
}
```
## POST /generate-pdf
With a proper JWT topken as ```Authorization Bearer tokencontent```
the endpoint will return a PDF file according to the HTML description

# Configuration
The application will require two environmental variables:
```
SECRET_KEY = key string that will be used to sign the Jwt token
API_KEY = key that the client applications use to authorize their access to the service
```


# Author
Petteri Loisko 
petteri.loisko@gmail.com
25.8.2025
