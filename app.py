from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import uuid

from io import StringIO
import re

# from calculate import parse_number, filter_input

# from flask import Flask
# from flask import request
# from flask import jsonify
# import json
from io import StringIO

import pandas as pd

import numpy as np
import re


def parse(x):
    """
	The parser of pairs
	"""

    y = re.search("\((.*),(.*)\)", x).group(1, 2)

    if y:
        return y[0], y[1]

    return None, None


def parse_number(x):
    """
	Accept int and float only
	"""

    try:
        y = re.match("^\((\d*\.?\d*),(\d*\.?\d*)\),?$", x).group(1, 2)

        if y:
            return y[0], y[1]
    except AttributeError:
        return None, None


def catch(func, handle=lambda e: e, show_err=True, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if not show_err:
            return handle(e)
        else:
            pass


def convt_float(x):
    try:
        return float(x[0]), float(x[1])
    except ValueError:
        return False


def filter_input(x):
    """
	Turn list of tuple to 2 den df
	Filter out None from the raw input
	Convert each column to number
	Return numpy array
	"""

    df = pd.DataFrame(x, columns=["A", "B"])
    df = df[~df["A"].isnull()]
    df["A"] = pd.to_numeric(df["A"])
    df["B"] = pd.to_numeric(df["B"])
    # result = df.to_records(index=False)
    result = df.to_numpy()
    return result


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "stackbox"


@app.route("/")
@cross_origin()
def home():
    return send_from_directory("/app", "index.html")


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
        # print("message is" + message.value.decode("utf-8"))
        raw_input = [parse_number(message.value.decode("utf-8"))]
        final_input = filter_input(raw_input)
        cov_matrix = np.cov(final_input)
        # jason.dumps only accpept str, convert result into str
        result = np.array2string(cov_matrix, precision=16)
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
