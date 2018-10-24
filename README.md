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
