FROM python:3.9-slim

WORKDIR /app
COPY *.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV CLOUDFLARE_EMAIL <email>
ENV CLOUDFLARE_API_KEY <api_key>
ENV CLOUDFLARE_ZONE_ID <zone_id>
ENV CLOUDFLARE_DNS_RECORDS <dns_records>

CMD ["python", "-u", "main.py"]