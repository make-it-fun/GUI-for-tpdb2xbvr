from tpdb2xbvr import handle_request, search, get_xtras, get_scene
from main import get_config, calculate_age
from pathlib import Path
import json
from datetime import (date)

import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        Path(Path.cwd() / 'data').mkdir(exist_ok=True)
        config = get_config('../config.json')
        api_key = config['key']
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # self.url = 'https://api.metadataapi.net/scenes/wankz-vr-hello-neighbor'
        # self.url = 'https://api.metadataapi.net/scenes/wankz-vr-wankzvr-car-wash-1'
        self.url = 'https://api.metadataapi.net/scenes/wankz-vr-paddys-pub'

    def test_handle_request(self):

        res = handle_request(self.url, headers=self.headers)
        print(f'result: {res}')
        if res is not None:
            with open('data/test_handle_request.json', 'w') as outfile:
                json.dump(res, outfile)

        with open('data/test_handle_request.json') as request_file:
            req = json.load(request_file)
        self.assertEqual('Paddys Pub', req['data']['title'])

    def test_get_scene(self):
        # test using requests response
        res = handle_request(self.url, headers=self.headers)
        print(f'result: {res}')
        if res is not None:
            scene = get_scene(url_or_response=res, headers=self.headers)
            self.assertEqual('Paddys Pub', scene['scenes'][0]['title'])
        else:
            self.fail(f'Failed to get result from "handle_request()" with {self.url}')

        # test using url
        scene = get_scene(url_or_response=self.url, headers=self.headers)
        if scene is not None:
            self.assertEqual('Paddys Pub', scene['scenes'][0]['title'])
        else:
            self.fail(f'Failed to get scene from "get_scene()" with {self.url}')

    def test_get_xtras(self):
        xtras = get_xtras(self.url, headers=self.headers)
        for name, vals in xtras.items():
            age = calculate_age(vals['dob'])
            dob = vals['dob']
            print(f'{name} was born on {dob} and is currently {age}')
        self.assertEqual(date.fromisoformat('1990-02-03'), xtras['Trinity St Clair']['dob'])
        self.assertEqual(date.fromisoformat('1997-04-20'), xtras['Alex Grey']['dob'])
        self.assertEqual(
            'https://thumb.metadataapi.net/unsafe/1000x1500/smart/filters:sharpen():upscale()/https%3A%2F%2Fcdn.metadataapi.net%2Fperformer%2Ffe%2F73%2F9b%2F6c623e650bdc7590ca091f32bdb1621%2Fposter%2Falex-grey.jpg',
            xtras['Alex Grey']['artist_posters'][3])
        self.assertEqual(
            'https://thumb.metadataapi.net/unsafe/1000x1500/smart/filters:sharpen():upscale()/https%3A%2F%2Fcdn.metadataapi.net%2Fperformer%2F39%2F6f%2Fb6%2Fe8d455f18438eb462a64125d83bb5cd%2Fposter%2Ftrinity-st-clair.jpg',
            xtras['Trinity St Clair']['artist_posters'][1])

    def test_search(self):
        query = 'czech vr dellai'
        res = search(query, headers=self.headers)
        print(res)
        if res is not None:
            with open('data/search.json', 'w') as outfile:
                json.dump(res, outfile)


if __name__ == '__main__':
    unittest.main()
