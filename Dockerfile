FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV LM_STUDIO_BASE_URL=http://host.docker.internal:1234/v1
ENV LM_STUDIO_API_KEY=lm-studio
ENV DEV_FAST_MODE=true

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]