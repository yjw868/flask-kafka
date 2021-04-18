import json
from flask import Flask, session, request, json as flask_json
from flask_socketio import (
    SocketIO,
    send,
    emit,
    join_room,
    leave_room,
    Namespace,
    disconnect,
)


def test_info(client):
    response = client.get("/")
    result = response.get_json()
    # assert result is not None
    assert "message" in result
    assert result["message"] == "It Works"


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)
disconnected = None


@socketio.on("connect")
def on_connect():
    if request.args.get("fail"):
        return False
    send("connected")
    send(json.dumps(request.args.to_dict(flat=False)))
    send(
        json.dumps(
            {
                h: request.headers[h]
                for h in request.headers.keys()
                if h not in ["Host", "Content-Type", "Content-Length"]
            }
        )
    )


@socketio.on("disconnect")
def on_disconnect():
    global disconnected
    disconnected = "/"


@socketio.event(namespace="/test")
def connect():
    send("connected-test")
    send(json.dumps(request.args.to_dict(flat=False)))
    send(
        json.dumps(
            {
                h: request.headers[h]
                for h in request.headers.keys()
                if h not in ["Host", "Content-Type", "Content-Length"]
            }
        )
    )


@socketio.on("disconnect", namespace="/test")
def on_disconnect_test():
    global disconnected
    disconnected = "/test"

