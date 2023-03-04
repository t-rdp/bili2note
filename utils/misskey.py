from mipac.client import Client
from .get_config import GetConfig
config = GetConfig()

async def post(text, files=[]):
    client = Client(config["MISSKEY"]["BaseUrl"], config["MISSKEY"]["AccessToken"])
    await client.http.login()
    api = client.api
    note = await api.note.action.send(text, files=files)
    await client.http.close_session()
    return note

async def upload(path):
    client = Client(config["MISSKEY"]["BaseUrl"], config["MISSKEY"]["AccessToken"])
    await client.http.login()
    api = client.api
    file = await api.drive.file.action.upload_file(path)
    await client.http.close_session()
    return file
