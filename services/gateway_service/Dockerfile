FROM python:3.10-alpine

#Change working directory
WORKDIR /code
COPY ./services/gateway_service /code
COPY ./lib/utils /code/app
COPY ./lib/custom_exceptions /code/app
COPY ./lib/kafka_utils/ /code/app
RUN pip3.10 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "app/main.py"]
