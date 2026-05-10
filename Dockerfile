FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv

COPY --chown=appuser:appuser app ./app

USER appuser

EXPOSE 8000 

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]