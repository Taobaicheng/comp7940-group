FROM python:3.11-slim

WORKDIR /APP
COPY requirements.txt .
RUN pip install --nocache-dir -r requirements.txt
COPY ..
EXPOSE $PORT
CMD ["python","Trip_AIbot.py","--host=0.0.0.0"]
