from flask import Flask, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    html_content = request.data.decode('utf-8')
    pdf_io = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=False, download_name='report.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    