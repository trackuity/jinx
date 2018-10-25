# jinx

Fast and simple indexing for [JSON Lines](http://jsonlines.org/) files, complete with
a built-in [Sanic](https://sanic.readthedocs.io) web server for speedy lookups over HTTP. 
[Berkeley DBs](https://pypi.org/project/bsddb3/) are used under the hood for the indexes.

For trying **jinx** out on an Ubuntu machine, you can get started like so:

```sh
$ apt-get install libdb5.3-dev

$ virtualenv --python=python3 env
$ env/bin/python setup.py develop

$ env/bin/jinx --help
```

On a Mac, you might want to use **brew** to install **berkeley-db** and then point to it 
using the BERKELEYDB_DIR environment variable while executing setup.py, e.g.:

```sh
BERKELEYDB_DIR=/usr/local/opt/berkeley-db@4/ env/bin/python setup.py develop
```

Once you got this sorted, you're ready to jinx some files. Here's a simple example:

```sh
$ cat players.jsonl
{"name": "lukaku", "country": "belgium",  "goals": 73, "matches": 80}
{"name": "hazard", "country": "belgium", "goals": 53, "matches": 86}

$ env/bin/jinx index players.jsonl -k name
$ ls players.*
players.jsonl
players.jsonl.jinx

$ env/bin/jinx lookup players.jsonl hazard
{"name": "hazard", "country": "belgium", "goals": 53, "matches": 86}
$ env/bin/jinx lookup players.jsonl hazard lukaku
{"name": "hazard", "country": "belgium", "goals": 53, "matches": 86}
{"name": "lukaku", "country": "belgium", "goals": 73, "matches": 80}
```

You can also group your lookup keys by specifying a prefix field:

```sh
$ env/bin/jinx index players.jsonl -k name -p country

$ env/bin/jinx lookup players.jsonl belgium:hazard
{"name": "hazard", "country": "belgium", "goals": 53, "matches": 86}
$ env/bin/jinx lookup players.jsonl -p belgium hazard
{"name": "hazard", "country": "belgium", "goals": 53, "matches": 86}
```

And there's nifty built-in web server for doing lookups over HTTP as well:

```
$ env/bin/jinx serve -h 127.0.0.1 -p 8000 -d .

$ curl http://127.0.0.1:8000/players/belgium:hazard
[{"name":"hazard","country":"belgium","goals":53,"matches":86}]
$ curl http://127.0.0.1:8000/players/belgium/hazard
[{"name":"hazard","country":"belgium","goals":53,"matches":86}]
$ curl http://127.0.0.1:8000/players/belgium/hazard,lukaku
[{"name":"hazard","country":"belgium","goals":53,"matches":86},{"name":"lukaku","country":"belgium","goals":73,"matches":80}]
```

If you change your data while the web server is running, you can reload via a PATCH request:

```sh
$ curl -X PATCH http://127.0.0.1:8000/players
```

or simply:

```sh
$ curl -X PATCH http://127.0.0.1:8000
```

This gets even cooler when combined with using directories. When you have a directory like e.g.

```sh
$ ls players/
20181025.jsonl
20181025.jsonl.jinx
```

you can do lookups on the directory and **jinx** will automatically use the latest (indexed) JSON Lines
file in that directory (based on sorting them alphanumerically). So whenever you want to update your
data, you can simply add new files to the directory and switch atomically by sending a PATCH request.
And if you want to switch back to the old data, you can simply remove the new files and reload again.
