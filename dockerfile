FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    EXORA_BROWSER_HEADLESS=true \
    EXORA_PORT=8501

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt \
    && playwright install --with-deps chromium

COPY . .

# Run as a non-root user; /workspace is where the agent may read and write files
RUN useradd --create-home --uid 1000 exora \
    && mkdir -p /workspace && chown -R exora:exora /workspace /app \
    && chmod -R a+rX /ms-playwright
USER exora

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:%s/_stcore/health' % os.getenv('EXORA_PORT','8501'))" || exit 1

CMD ["sh", "-c", "streamlit run ui.py --server.address=0.0.0.0 --server.port=${EXORA_PORT:-8501} --server.headless=true"]
