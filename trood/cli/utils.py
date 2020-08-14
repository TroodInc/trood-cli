import os
import keyring
import click
from tabulate import tabulate
import requests
import json


def get_em_ulr(path):
    host = os.environ.get("EM", "em.tools.trood.ru")
    return f'https://{host}/{path}'

def save_token(token):
    keyring.set_password("trood/em", "active", token)


def get_token(ctx: click.Context = None) -> str:
    if ctx:
        token = ctx.obj.get('TOKEN')

        if token:
            return f'Token: {token}'

    try:
        token = keyring.get_password("trood/em", "active")

        if token:
            return f'Token: {token}'
        else:
            click.echo(f'You need to login first.')
    except Exception:
        click.echo(f'Keychain not supported, use --token flag for authorization')


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


def get_fixtures(fixtures_path):
    with open(fixtures_path) as json_file:
        fixtures = json.load(json_file)
    return fixtures


def apply_custodian_migrations(namespace, data, verbose, headers):
    result = requests.post(
        f'https://{namespace}.saas.trood.ru/custodian/migrations/',
        json=data["migration"],
        headers=headers
    )
    if result.status_code == 200:
        click.echo(f"Migration {data['migration']['id']} is uploaded.")
    elif result.status_code == 400 and result.json()["error"]["Code"] == "duplicated_value_error":
        click.echo(f"Duplicate. Migration {data['migration']['id']} is already applied.")
    else:
        click.echo(f"Failed to upload migration {data['migration']['id']}.")
        if verbose:
            click.echo(result.json())


def upload_custodian_record(namespace, data, verbose, headers):
    result = requests.post(
        f'https://{namespace}.saas.trood.ru/custodian/data/{data["object"]}/',
        json=data["data"],
        headers=headers
    )
    if result.status_code == 200:
        click.echo(f"Records of {data['object']} is uploaded.")
    else:
        click.echo(f"Failed to upload {data['object']} records.")
        if verbose:
            click.echo(result.json())


def upload_records(namespace, data, verbose, headers):
    result = requests.post(
        f'https://{namespace}.saas.trood.ru/{data["target"]}/api/v1.0/datas/',
        json=data,
        headers=headers
    )

    if result.status_code == 200:
        click.echo(f"Records of {data['object']} is uploaded.")
    else:
        click.echo(f"Failed to upload {data['object']} records.")
        if verbose:
            click.echo(result.json())


def apply_fixture(namespace, fixtures, verbose, token):
    headers = {'Authorization': token}
    for fixture in fixtures:
        if fixture['target'] == "custodian":
            for data in fixture["fixture"]:
                if data["type"] == "migration":
                    apply_custodian_migrations(namespace, data, verbose, headers)
                elif data["type"] == "record":
                    upload_custodian_record(namespace, data, verbose, headers)
        else:
            upload_records(namespace, data, verbose, headers)
