FROM python:3.12-slim

WORKDIR /app

# Dependencies dulu, biar layer ini di-cache (gak reinstall tiap kali ubah kode)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baru copy kode
COPY . .

# Default command (di-override di docker-compose.yml per service)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]