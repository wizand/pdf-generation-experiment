from email.mime import application
from flask import Flask, request, send_file
from weasyprint import HTML
import io
import os
import jwt
import random
from datetime import datetime, timezone, timedelta


SECRET_KEY = os.environ.get("SECRET_KEY", "NA")
API_KEY = os.environ.get("API_KEY", "NA")
app = Flask(__name__)


def generateToken(applicationId):
    payload = {
        "sub": applicationId + str(random.randint(1, 999999)),
        "aud": applicationId,
        "iss": "pdfapi",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
    }


    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def isAuthorized(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        print("No Authorization header found")
        return False

    if not auth_header.startswith("Bearer "):
        print("Invalid Authorization header format")
        return False

    token = auth_header.split(" ", 1)[1]
    if token is None:
        print("No token found")
        return False

    try:
        print("decoding token [" + token + "]")
        unverified_header = jwt.get_unverified_header(token)
        print("Header:", unverified_header)
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        print("Payload:", unverified_payload)
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"require": ["exp", "iss", "sub", "aud"], "verify_exp": True, "verify_aud": False})
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return False
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {str(e)}")
        return False
    except jwt.DecodeError:
        print("Decode error")
        return False

    return True



@app.route('/request-token', methods=['POST'])
def request_token():
    data = request.get_json(silent=False)
    if not data:
        return {"error": "Invalid request"}, 400
    
    apiKey = data.get("api-key")
    if ( apiKey is None ) or ( apiKey != API_KEY ):
        return {"error": "Unauthorized"}, 401
    
    applicationId = data.get("application-id")
    if ( applicationId is None):
        return {"error": "Unauthorized"}, 401
    
    token = generateToken(applicationId)

    return {"token": token}, 200





@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    if not isAuthorized(request):
        return {"error": "Unauthorized"}, 401

    html_content = request.data.decode('utf-8')
    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=False, download_name='report.pdf')

if __name__ == '__main__':
    if SECRET_KEY == "NA":
        print("No SECRET_KEY environmental variable found..quitting")
        exit()
    if API_KEY == "NA":
        print("No API_KEY environmental variable found..quitting")
        exit()
    app.run(host='0.0.0.0', port=5000)
    

