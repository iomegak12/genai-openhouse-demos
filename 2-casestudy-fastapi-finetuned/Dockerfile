FROM python:alpine

LABEL environment=Production
LABEL author=Ramkumar.JD
LABEL company=REDIVAC

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ARG HOST=0.0.0.0
ARG PORT=8001

ENV UVICORN_HOST=${HOST:-0.0.0.0}
ENV UVICORN_PORT=${PORT:-8001}

ENTRYPOINT ["python", "main.py"]