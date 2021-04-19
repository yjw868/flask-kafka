from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import uuid
from io import StringIO
import re

# from mypkg.calculate import parse_number, filter_input
from mypkg.calculate import calculate_cov_matrix

import pandas as pd
import numpy as np


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "stackbox"


@app.route("/")
@cross_origin()
def home():
    return send_from_directory("/app/app", "index.html")


""" Kafka endpoints """


@socketio.on("connect", namespace="/kafka")
def test_connect():
    emit("logs", {"data": "Connection established"})


@socketio.on("kafkaconsumer", namespace="/kafka")
def kafkaconsumer(message):
    consumer = KafkaConsumer(group_id="consumer-1", bootstrap_servers=BOOTSTRAP_SERVERS)
    tp = TopicPartition(TOPIC_NAME, 0)
    # register to the topic
    consumer.assign([tp])

    # obtain the last offset value
    consumer.seek_to_end(tp)
    lastOffset = consumer.position(tp)
    consumer.seek_to_beginning(tp)
    emit("kafkaconsumer1", {"data": ""})

    for message in consumer:
        # # print("message is" + message.value.decode("utf-8"))
        # raw_input = [parse_number(message.value.decode("utf-8"))]
        # final_input = filter_input(raw_input)
        # cov_matrix = np.cov(final_input)
        # # jason.dumps only accpept str, convert result into str
        # result = np.array2string(cov_matrix, precision=16)
        result = calculate_cov_matrix(message)
        emit(
            "kafkaconsumer",
            {"data": message.value.decode("utf-8") + " covariance matrix is " + result},
        )
        # emit(
        #     "kafkaconsumer",
        #     {
        #         "data": message.value.decode("utf-8")
        #         + str(type(message.value.decode("utf-8")))
        #     },
        # )
        # emit("kafkaconsumer", {"data": message.value.decode("utf-8")})
        if message.offset == lastOffset - 1:
            break
    consumer.close()


@socketio.on("kafkaproducer", namespace="/kafka")
def kafkaproducer(message):
    print(TOPIC_NAME)
    print(BOOTSTRAP_SERVERS)
    print(message)
    print(type(message))
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    producer.send(
        TOPIC_NAME,
        value=bytes(str(message), encoding="utf-8"),
        key=bytes(str(uuid.uuid4()), encoding="utf-8"),
    )

    emit("logs", {"data": "Added " + message + " to topic"})
    emit(
        "kafkaproducer", {"data": message},
    )
    producer.close()
    kafkaconsumer(message)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True, log_output=True)
