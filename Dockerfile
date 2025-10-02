FROM python:3.11-slim

WORKDIR /app

# Optional: curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and model files (must exist next to this Dockerfile)
COPY streamlit_app.py .
COPY linear_regression.joblib feature_columns.json . 

# (optional) copy the rest if needed
# COPY . .

# Verify model files exist in the image
RUN test -f /app/linear_regression.joblib && test -f /app/feature_columns.json

# Environment for Cloud Run and model location
ENV PORT=8080
ENV MODEL_DIR=/app
EXPOSE 8080

# Healthcheck (optional)
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1

# Single CMD only
CMD ["bash", "-lc", "streamlit run streamlit_app.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]