FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info\
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*
			
# Install Python deps
RUN pip install flask weasyprint gunicorn
    
# Copy app
COPY pdfapi.py /pdfapi.py
			
# Expose port
EXPOSE 5000
# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "pdfapi:app"]