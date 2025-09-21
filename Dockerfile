FROM python:3.11-slim

# 1) System prep
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 2) Workdir
WORKDIR /app

# 3) Install deps first (better cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy app + data
COPY app.py ./app.py
COPY data ./data

# 5) Streamlit server settings
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]