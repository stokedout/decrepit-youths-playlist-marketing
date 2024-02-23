FROM python:3

WORKDIR /app

COPY ./extractor.py /app/extractor.py
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["python","/app/main.py"]