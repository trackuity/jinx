import bsddb3
import struct
import json
import sys

from sanic import Sanic, response
from .io import Database


app = Sanic(__name__)
app.config.DATA_DIR = '.'

databases = {}


@app.route('/<name>/<keys>')
@app.route('/<name>/<prefix>/<keys>')
async def lookup(request, name, keys, prefix=None):
    database = databases.get(name)
    if database is None:
        databases[name] = database = Database(name, data_dir=app.config.DATA_DIR)
    keys = keys.split(',')
    if prefix is not None:
        keys = ('{0}:{1}'.format(prefix, key) for key in keys)
    return response.json(database.multi_get(keys))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
