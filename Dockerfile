FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY app/ app/
COPY model/model.pkl model/model.pkl

# Run as a non-root user (security best practice)
RUN useradd -m appuser
USER appuser

ARG MODEL_VERSION=dev
ENV MODEL_VERSION=${MODEL_VERSION}

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
