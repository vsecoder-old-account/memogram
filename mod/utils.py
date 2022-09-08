# Utils
import base64
import binascii
import os


def encode_bs64(b):
    return base64.decodebytes(bytes(b, "utf-8"))


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
