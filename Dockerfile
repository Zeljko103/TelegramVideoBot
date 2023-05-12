FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

COPY video.py /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app


CMD ["python", "video.py"]
