import requests
from bs4 import BeautifulSoup
import threading
import json
import os

URL = 'https://mcversions.net/'
JSON_FILE = 'src/vanilla/data/vanilla_versions.json'


class VanillaManager:
    def __init__(self):
        self.versions = []
        self.versions_lock = threading.Lock()
        self.URL = URL
        if not os.path.exists(JSON_FILE):
            self.scrap_vanilla()
            self._save_json()
        else:
            self._load_json()

    def scrap_vanilla(self):
        response = requests.get(self.URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        version_elements = soup.find_all(
            lambda tag: tag.has_attr('data-version'))

        versions = map(lambda el: el['data-version'], version_elements)
        threads = []

        def filter_versions(tag):
            return all(map(lambda digit: digit.isdigit(),  tag.split('.')))

        filtered_versions = list(filter(filter_versions, versions))

        for version in filtered_versions:
            new_thread = threading.Thread(
                target=self.get_download_version, args=(version,))
            threads.append(new_thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def get_download_version(self, version):
        url = self.URL + 'download/' + version
        print(f'GET {url}')

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            download_element = soup.find(
                lambda tag: tag.string == 'Download Server Jar')
            link = download_element['href']
            dict = {'version': version, 'download': link}
            self.append_version(dict)
        except:
            pass

    def append_version(self, version):
        with self.versions_lock:
            self.versions.append(version)

    def _save_json(self):
        with self.versions_lock:
            with open(JSON_FILE, 'w') as json_file:
                json.dump(self.versions, json_file)

    def _load_json(self):
        with open(JSON_FILE, 'r') as json_file:
            self.versions = json.load(json_file)


vanilla = VanillaManager()
vanilla.scrap_vanilla()
