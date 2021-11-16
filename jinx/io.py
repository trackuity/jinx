import os
import json
import bsddb3
import struct


class Indexer:

    def __init__(self, name, key_field, prefix_fields=None):
        self._key_field = key_field
        self._prefix_fields = prefix_fields
        self._file = open(name, 'r')
        self._db = bsddb3.hashopen(name + '.jinx', 'c')
        self._offset = 0

    def index(self):
        for line in self._file:
            data = json.loads(line)
            key = data[self._key_field]
            if self._prefix_fields is not None:
                prefix_key = ",".join(
                    data[prefix_field] for prefix_field in self._prefix_fields
                )
                key = '{0}:{1}'.format(prefix_key, key)
            self._db[bytes(key, 'utf-8')] = struct.pack('L', self._offset)
            self._offset += len(line)

    def close(self):
        self._file.close()
        self._db.close()


class Database:

    def __init__(self, name, data_dir='.'):
        path = os.path.join(data_dir, name)
        if os.path.isdir(path):  # when directory, pick last member alphanumerically
            filename = sorted(f for f in os.listdir(path) if f.endswith('.jinx'))[-1][:-5]
            path = os.path.join(path, filename)
        else:
            for ext in ('', '.json', '.jsonl'):
                path = os.path.join(data_dir, name + ext)
                if os.path.exists(path + '.jinx'):
                    break
            else:
                raise ValueError('database does not exist')

        self._file = open(path, 'r')
        self._index = bsddb3.hashopen(path + '.jinx', 'r')

    def multi_get(self, keys):
        for key in keys:
            packed = self._index.get(bytes(key, 'utf-8'))
            if packed is not None:
                offset = struct.unpack('L', packed)[0]
                self._file.seek(offset)
                yield self._file.readline()[:-1]  # don't include newline

    def close(self):
        self._file.close()
        self._index.close()
