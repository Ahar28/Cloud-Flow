FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 6001

ENTRYPOINT ["python"]

CMD ["app.py"]