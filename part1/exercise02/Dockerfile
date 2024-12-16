FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY projectv0_1.py .

EXPOSE 5000

CMD ["python", "projectv0_1.py"]
