FROM dhi.io/python:3.14-dev AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data

FROM dhi.io/python:3.14

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /venv /venv

COPY --from=builder --chown=65532:65532 /data /data

COPY --from=builder --chown=65532:65532 /build/app/ /app/

COPY --from=builder --chown=65532:65532 /build/scripts/ /app/scripts/

EXPOSE 8000

USER 65532:65532

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
