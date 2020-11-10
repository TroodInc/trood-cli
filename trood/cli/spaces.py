import os
import json
import zipfile
import click
import requests
from time import strftime, gmtime

from trood.cli import utils
from trood.cli.utils import get_em_ulr


@click.group()
def space():
    pass


@space.command()
@click.pass_context
def ls(ctx):
    result = requests.get(
        get_em_ulr('api/v1.0/spaces/'),
        headers={"Authorization": utils.get_token(ctx=ctx)}
    )

    if result.status_code == 200:
        utils.list_table(result.json())


@space.command()
@click.argument('space_alias')
@click.pass_context
def rm(ctx, space_alias):
    click.confirm(f'Do you want to remove space #{space_alias} ?', abort=True)

    result = requests.get(get_em_ulr('api/v1.0/spaces/'), headers={"Authorization": utils.get_token(ctx=ctx)})
    spaces = json.loads(result.text)

    for space in spaces:
        if space['alias'] == space_alias:
            space_id = space['id']

    result = requests.delete(
        get_em_ulr(f'api/v1.0/spaces/{space_id if space_id else space_alias}/'),
        headers={"Authorization": utils.get_token(ctx=ctx)}
    )

    if result.status_code == 204:
        click.echo(f'Space #{space_alias} removed successfully!')


@space.command()
@click.argument('name')
@click.option('--template', default='default')
@click.pass_context
def create(ctx, name: str, template: str):
    response = requests.get(
        get_em_ulr(f'api/v1.0/market/spaces/{template}/'),
        headers={"Authorization": utils.get_token(ctx=ctx)},
    )

    if response.status_code == 200:
        data = response.json()
        prompts = {}

        for k, v in data['prompts'].items():
            is_password = v['type'] == 'password'
            prompts[k] = click.prompt(v['question'], hide_input=is_password, confirmation_prompt=is_password)

        result = requests.post(
            get_em_ulr('api/v1.0/spaces/'),
            headers={"Authorization": utils.get_token()},
            json={'name': name, 'template': template, 'prompts': prompts}
        )

        if result.status_code == 201:
            data = result.json()
            click.echo(f'Space {data["data"]["url"]} created successfully! ')
        elif result.status_code == 400:
            data = result.json()
            click.echo(data['msg'])
    else:
        click.echo(f'Cant create space from [{template}] template')


@space.command()
@click.argument('application')
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.pass_context
def publish(ctx, application, path):
    if ctx and not ctx.obj.get('FORCE'):
        click.confirm(f'Do you want to publish "{path}" to your app #{application}?', abort=True)

    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                fp = os.path.join(root, file)
                zp = fp.replace(path, '')

                ziph.write(filename=fp, arcname=zp)

    time = strftime("%Y-%m-%d__%H-%M-%S", gmtime())

    zipf = zipfile.ZipFile(f'{application}-{time}.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(path, zipf)
    zipf.close()

    result = requests.get(get_em_ulr('api/v1.0/applications/'), headers={"Authorization": utils.get_token(ctx=ctx)})
    apps = json.loads(result.text)

    app_id = None
    for app in apps:
        if app['alias'] == application:
            app_id = app['id']

    if not app_id:
        click.echo(f'Error while publishing: web app {application} does not exist', err=True)
    else:
        result = requests.post(
            get_em_ulr('api/v1.0/bundles/'),
            headers={"Authorization": utils.get_token(ctx=ctx)},
            data={"application": app_id},
            files={'file': open(f'{application}-{time}.zip', 'rb')}
        )

        if result.status_code == 201:
            click.echo(f'Web app {application} successfuly published')
        else:
            click.echo(f'Error while publishing: {result.content}', err=True)