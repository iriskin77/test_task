FROM python:3.10-slim

RUN mkdir /test_task

WORKDIR /test_task

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod a+x ./start.sh
