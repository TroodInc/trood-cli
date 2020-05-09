import keyring
import click
from tabulate import tabulate


def save_token(token):
    keyring.set_password("trood/em", "active", token)


def get_token(ctx: click.Context = None) -> str:
    token = ctx.obj.get('TOKEN') if ctx and 'TOKEN' in ctx.obj else keyring.get_password("trood/em", "active")
    if token:
        return f'Token: {token}'
    else:
        click.echo(f'You need to login first.')


def clean_token():
    keyring.delete_password("trood/em", "active")


def list_table(items):
    if len(items):
        headers = items[0].keys()

        data = [i.values() for i in items]

        click.echo(tabulate(data, headers=headers))
        click.echo()
    else:
        click.echo('----------------- nothing to show')
