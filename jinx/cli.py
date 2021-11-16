import click

from .io import Indexer, Database
from .server import app


@click.group()
def cli():
    pass


@click.command()
@click.option('--key', '-k', help='Key field.')
@click.option('--prefix', '-p', multiple=True, help='Prefix field.')
@click.argument('file')
def index(key, prefix, file):
    indexer = Indexer(file, key_field=key, prefix_fields=prefix)
    indexer.index()
    indexer.close()


@click.command()
@click.option('--prefix', '-p', multiple=True, help='Prefix to prepend to keys.')
@click.argument('file')
@click.argument('key', nargs=-1)
def lookup(prefix, file, key):
    if prefix is not None:
        key = ('{0}:{1}'.format(",".join(prefix), k) for k in key)
    database = Database(file)
    for value in database.multi_get(key):
        click.echo(value)
    database.close()


@click.command()
@click.option('--host', '-h', default='127.0.0.1', help='Server host.')
@click.option('--port', '-p', default=8000, help='Server port.')
@click.option('--workers', '-w', default=1, help='Number of workers.')
@click.option('--directory', '-d', default='.', help='Data directory.')
def serve(host, port, workers, directory):
    app.config.DATA_DIR = directory
    app.run(host=host, port=port, workers=workers)


cli.add_command(index)
cli.add_command(lookup)
cli.add_command(serve)


if __name__ == '__main__':
    cli()
