FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY todo.py .
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "todo.py"]
