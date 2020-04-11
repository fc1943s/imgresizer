FROM python:3.8.2-alpine3.11
WORKDIR /app

RUN apk add build-base zlib-dev jpeg-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENTRYPOINT ["python3"]
CMD ["-m", "unittest", "tests.py"]

