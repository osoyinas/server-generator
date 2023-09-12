""" 
vanilla_manager.py
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

from src.manager import Manager

URL = 'https://mcversions.net/'
JSON_FILE = 'src/vanilla/data/vanilla_versions.json'


class VanillaManager(Manager):
    """
    Inherits from Manager, scrap the versions from URL and load data in JSON_FILE
    """

    def __init__(self) -> None:
        """Constructor
        """
        super().__init__(url=URL, json_file=JSON_FILE)
        if not os.path.exists(self._json_file):
            self._scrap()
            self._save_json()
        else:
            self._load_json()

    def _scrap(self):
        try:

            response = requests.get(self._url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print(f"The requested {self._url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'html.parser')
        version_elements = soup.find_all(
            lambda tag: tag.has_attr('data-version'))

        versions = map(lambda el: el['data-version'], version_elements)

        def filter_versions(tag):
            return all(map(lambda digit: digit.isdigit(),  tag.split('.')))

        filtered_versions = list(filter(filter_versions, versions))
        with ThreadPoolExecutor(max_workers=5) as executor:
            for version in filtered_versions:
                executor.submit(self._get_version_download, version)

    def _get_version_download(self, version):
        url = self._url + 'download/' + version
        print(f'GET {url}')

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            download_element = soup.find(
                lambda tag: tag.string == 'Download Server Jar')
            if hasattr(download_element, 'href'):
                link = download_element['href']
                self._append_version({'version': version, 'download': link})
        except requests.exceptions.Timeout:
            print(f"The requested {self._url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")
            sys.exit(1)

    def _get_command(self, jar_name):
        return f'java -Xms4G -Xmx8G  -jar {jar_name} nogui'

    @staticmethod
    def get_name() -> str:
        """Returns manager name

        Returns:
            str: name
        """
        return "Vanilla"
