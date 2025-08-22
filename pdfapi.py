from flask import Flask, request, send_file
from weasyprint import HTML
import io
import os

EXPECTED_TOKEN = os.environ.get("SECRET_TOKEN", "NA")
app = Flask(__name__)


def isAuthorized(request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False
    
    if not auth_header.startswith("Bearer "):
        return False
    
    token = auth_header.split(" ", 1)[1]
    if token is None:
        return False
    
    return token == EXPECTED_TOKEN


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    
    if ( isAuthorized(request) == False ):
        return "Unauthorized", 401
    
    
    html_content = request.data.decode('utf-8')
    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=False, download_name='report.pdf')

if __name__ == '__main__':
    if EXPECTED_TOKEN == "NA":
        print("NO SECRET TOKEN SET. CANNOT CONTINUE")
        exit()
    app.run(host='0.0.0.0', port=5000)

