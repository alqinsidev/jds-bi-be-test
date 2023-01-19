FROM python:3.10-slim-bullseye

RUN mkdir /app

WORKDIR /app

COPY requirement.txt /app/requirement.txt

RUN pip3 install -r requirement.txt

COPY . /app/

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=2701"]