import collections
import json
import pathlib
import shutil

from urllib.request import urlopen


source_url = "http://veyepar.nextdayvideo.com/main/C/depy/S/depy_2016.json"
data_path = pathlib.Path('data.json')


if not data_path.exists():
    print("data.json not present. Downloading it from {}".format(source_url))
    with urlopen(source_url) as fp:
        data_path.write_bytes(fp.read())

data = {}
with open(str(data_path), encoding='utf-8') as fp:
    data = json.load(fp)

container = pathlib.Path('depy2016') / 'videos'
shutil.rmtree(str(container))
container.mkdir()

for episode in data:
    fields = episode['fields']
    video_url = fields.get('host_url')
    released = fields.get('released', False)
    if episode['model'] != "main.episode" or not video_url or not released or fields['state'] != 11:
        continue
    print(fields['slug'])
    file_ = container / (fields['slug'] + '.json')
    output = collections.OrderedDict([
        ('category', 'DePy 2016'),
        ('slug', fields['slug'].lower()),
        ('title', fields['name']),
        ('summary', ''),
        ('description', fields['description']),
        ('quality_notes', ''),
        ('language', 'English'),
        ('copyright_text', ''),
        ('thumbnail_url', 'https://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_url.split('/')[-1])),
        ('duration', None),
        ('videos', [{
            'type': 'youtube',
            'url': video_url,
            'length': None,
        }]),
        ('source_url', video_url),
        ('tags', []),
        ('speakers', fields['authors'].split(', ')),
        ('recorded', fields['start'].split('T')[0]),
    ])
    file_.write_text(json.dumps(output, indent='  '))
