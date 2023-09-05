""" 
vanilla_manager.py
"""
import threading
import os
import sys
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
        if not os.path.exists(self.json_file):
            self._scrap()
            self._save_json()
        else:
            self._load_json()

    def _scrap(self):
        try:

            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print(f"The requested {self.url} has exceed the timeout.")
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

        for version in filtered_versions:
            new_thread = threading.Thread(
                target=self._get_version_download, args=(version,))
            self.threads.append(new_thread)

        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def _get_version_download(self, version):
        url = self.url + 'download/' + version
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
            print(f"The requested {self.url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")
            sys.exit(1)

    @staticmethod
    def get_name() -> str:
        """Returns manager name

        Returns:
            str: name
        """
        return "Vanilla"
