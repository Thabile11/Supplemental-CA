FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home --uid 10002 adminuser
USER adminuser

EXPOSE 5001
CMD ["python", "app.py"]
