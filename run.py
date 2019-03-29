#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask
from app import init

__all__ = ['app_server', "init_server"]

app_server = Flask(__name__)


def init_server():
    init(app_server)


if __name__ == '__main__':
    init_server()
    app_server.run(host='0.0.0.0', port=8000)
