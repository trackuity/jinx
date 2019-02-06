import bsddb3
import struct
import json
import sys

from sanic import Sanic, response
from .io import Database


app = Sanic(__name__)
app.config.DATA_DIR = '.'

databases = {}


@app.route('/<name>/<keys:path>', methods=['GET'])
@app.route('/<name>/<prefix:[^:]>/<keys:path>', methods=['GET'])
async def lookup(request, name, keys, prefix=None):
    database = databases.get(name)
    if database is None:
        databases[name] = database = Database(name, data_dir=app.config.DATA_DIR)
    keys = keys.split(',')
    if prefix is not None:
        keys = ('{0}:{1}'.format(prefix, key) for key in keys)
    return response.json(database.multi_get(keys))


@app.route('/', methods=['PATCH'])
@app.route('/<name>', methods=['PATCH'])
async def reload(request, name=None):
    if name is None:
        databases.clear()
    elif name in databases:
        del databases[name]
    return response.text('', status=204)  # no content


@app.route('/_ping', methods=['GET'])
async def ping(request):
    return response.text('pong')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
