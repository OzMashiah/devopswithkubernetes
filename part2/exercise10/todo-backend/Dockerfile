FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY todo-backend.py .

EXPOSE 5001

CMD ["python", "todo-backend.py"]
