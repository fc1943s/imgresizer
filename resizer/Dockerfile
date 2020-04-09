FROM python:3.8.2-alpine3.11
WORKDIR /app

RUN apk add build-base zlib-dev jpeg-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN python -m unittest discover

ENTRYPOINT ["python3"]
CMD ["src/app.py"]

