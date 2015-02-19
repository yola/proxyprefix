import os
import sys

from flask import Flask, url_for


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from proxyprefix.wsgi import ReverseProxiedApp  # noqa


app = Flask(__name__)


@app.route('/show_path')
def show_path():
    return url_for('.show_path')


if __name__ == '__main__':
    app.wsgi_app = ReverseProxiedApp(app.wsgi_app)
    app.debug = True
    app.run()
