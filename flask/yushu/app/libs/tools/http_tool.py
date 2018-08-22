import requests


class HTTP(object):
    @staticmethod
    def get(url, return_json=True):
        response = requests.get(url=url)
        if response.status_code != 200:
            return {} if return_json else ''
        else:
            return response.json()
