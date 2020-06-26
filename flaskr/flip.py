import argparse
import base64
import numpy as np
import cv2
from datauri import DataURI
from flask_socketio import SocketIO
from flask import Flask, render_template, request
import socketio
from engineio.payload import Payload

app = Flask(__name__)
socketio_server = SocketIO(app)
sioclient = socketio.Client()
Payload.max_decode_packets = 500

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@socketio_server.on('connect', namespace='/web')
def connect_web():
    print('[INFO] Web client connected: {}'.format(request.sid))


@socketio_server.on('disconnect', namespace='/web')
def disconnect_web():
    print('[INFO] Web client disconnected: {}'.format(request.sid))


@socketio_server.on('frame', namespace='/web')
def get_frame(message):
    socketio_server.emit('flipped', convert_image_to_jpeg(message), namespace='/web')
    print("sent")


def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def convert_image_to_jpeg(image):
    # datauri to opencv reading format
    cv_image = data_uri_to_cv2_img(image)

    # open cv flip
    flipHorizontal = cv2.flip(cv_image, 1)

    # reformat to jpg
    (turn_jpg, buffer) = cv2.imencode('.jpg', flipHorizontal)
    # ensure the frame was successfully encoded
    if not turn_jpg:
        pass

    # encode image to 64 base
    jpg_as_text = base64.b64encode(buffer)
    jpg_original = base64.b64decode(jpg_as_text)

    # reformat into datauri
    return DataURI.make('image/jpeg', charset='utf-8', base64=True, data=jpg_original )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)
