import datetime
import html
import json
import requests
import sys
from typing import Union, Optional

headers = {}


def search(query: str, headers: dict) -> Optional[requests.Response.json]:
    """
    searches ThePornDB API for scenes
    :param query: A search string such as 'czech vr dellai'
    :param headers: headers including api key
    :return: response object

    documentation is here: https://metadataapi.net/docs
    """

    q = query.split()  #
    q = '+'.join(q)

    # https://api.metadataapi.net/scenes?parse=asperiores&q=illum&hash=qui&limit=1
    url = 'https://api.metadataapi.net/scenes?q=' + q
    print(f'*** search ***\nrequesting url: {url}\n')
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return None


def handle_request(url, headers) -> Optional[requests.Response.json]:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        return None


# noinspection PyTypeChecker
def get_xtras(url_or_response: Union[str, list], headers) -> Optional[dict]:
    if type(url_or_response) == str:
        response = handle_request(url_or_response, headers)
    else:
        response = url_or_response
    if response:
        xtras = {}

        for p in response['data']['performers']:
            name = p['name']
            try:
                birthday = datetime.date.fromisoformat(p['parent']['extras']['birthday'])
            except Exception as e:
                print(e)
                birthday = None

            xtras[name] = {
                'artist_posters': [],
                'dob': birthday,
                'images': {}
            }

            try:
                for poster in p['parent']['posters']:
                    xtras[name]['artist_posters'].append(poster['url'])
            except TypeError as e:
                print(e)
                xtras[name]['artist_posters'] = []

            xtras[name]['dob'] = birthday

        return xtras
    else:
        print('get_xtras() there is a problem with the response')
        return None


def get_scene(url_or_response, headers) -> Optional[dict]:
    if type(url_or_response) == str:
        result = handle_request(url_or_response, headers)
    else:
        result = url_or_response

    if result:
        
        scene = {}
        res_data = result['data']

        scene['_id'] = res_data['id']
        scene['scene_id'] = str(res_data['_id'])
        scene['scene_type'] = 'VR'
        scene['title'] = res_data['title']
        scene['studio'] = res_data['site']['name']
        scene['site'] = res_data['site']['name']
        scene['covers'] = [res_data['image']]

        gallery = []
        if 'poster' in res_data:
            gallery.append(res_data['poster'])
        scene['gallery'] = gallery

        posters = []
        if 'posters' in res_data:
            res = res_data
            for key, value in res_data['posters'].items():
                posters.append(value)
        scene['posters'] = posters

        background = []
        if 'background' in res_data:
            for key, value in res_data['background'].items():
                background.append(value)
        scene['background'] = background

        if 'media' in res_data and res_data['media'] != None:
            if res_data['media']['url'] == None:
                scene['media'] = ''
            else:
                scene['media'] = res_data['media']['url']
        else:
            scene['media'] = ''

        tags = []
        for t in res_data['tags']:
            tags.append(t['name'])
        scene['tags'] = tags

        performer = []

        for t in res_data['performers']:
            performer.append(t['name'])

        scene['cast'] = performer

        scene['synopsis'] = html.unescape(res_data['description'])  # remove '&#039;' from description
        scene['released'] = res_data['date']
        scene['homepage_url'] = res_data['url']
        scene['duration'] = 1

        data = {}
        data['timestamp'] = datetime.datetime.now().isoformat() + 'Z'
        data['bundleVersion'] = '1'
        data['scenes'] = [scene]

        # additional metadata for actress
        # data['performer_posters'] = result['']
        return data
    else:
        return None


if __name__ == '__main__':

    api_key = ''  # insert ThePornDB api key here, get it from: https://metadataapi.net/user/api-tokens
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    if not api_key:
        print('please get an api token from https://metadataapi.net/user/api-tokens\nThen fill in the api_key variable')

    if len(sys.argv) > 1:
        url = sys.argv[1]
        req = handle_request(url, headers)
        res = get_scene(req, headers)
        # noinspection PyTypeChecker
        xtras = get_xtras(req, headers)
        if res is not None:
            with open('data/get_scene.json', 'w') as outfile:
                json.dump(res, outfile)
        if xtras is not None:
            with open('data/get_xtras.json', 'w') as outfile:
                json.dump(xtras, outfile)
