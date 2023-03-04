from .get_config import GetConfig
from .misskey import *
import asyncio
config = GetConfig()

def media_post(file):
  return asyncio.run(upload(file))

def TootPoster(data):
  """
  :data object: Return from media_downloader
  :return void
  """
  media_ids_arr = []

  if data['video_count'] is not None:
    data['plain'] = data['plain'] + '\n'+config['MISSKEY']['VideoSourcePrefix']+' ' + data['video_link']

  if data['image_count'] is not None:
    for id in range(1, min(data['image_count'], 5)):
      media_ids_arr.append(media_post('temp/img%d.png' % id))

  try:
    asyncio.run(post(data['plain'], media_ids_arr))
  except Exception:
    print(f'ERRO: failed to post')

if __name__ == '__main__':
  test_data = {'gif_count': 1, 'video_count': None, 'image_count': 3, 'plain': 'Tooting from python using `status_post` #mastodonpy !'}
  TootPoster(test_data)