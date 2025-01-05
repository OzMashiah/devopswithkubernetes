FROM python:3.9-slim

WORKDIR /usr/src/app

RUN pip install Flask

COPY dummysite.py ./dummysite.py

EXPOSE 8080

CMD ["python", "dummysite.py"]
