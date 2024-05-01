FROM tiangolo/uvicorn-gunicorn:python3.9-slim

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]