"""
spigot_manager.py
"""
import threading
import sys
import os
import requests

from bs4 import BeautifulSoup

from src.manager import Manager

URL = 'https://getbukkit.org/download/spigot'
JSON_FILE = 'src/spigot/data/spigot_versions.json'


class SpigotManager(Manager):
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
            print(f"GET {self._url}")
            response = requests.get(self._url, timeout=10)
            response.raise_for_status()  # Check if ok

        except requests.exceptions.Timeout:
            print(f"The requested {self._url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")
            sys.exit(1)
        soup = BeautifulSoup(response.text, 'html.parser')
        download_elements = soup.find_all(class_='download-pane')

        for element in download_elements:
            version = element.find('h2').text
            download_link_element = element.find('a', class_='btn-download')
            url = download_link_element['href']
            new_thread = threading.Thread(
                target=self._get_version_download, args=(version, url))
            self._threads.append(new_thread)

        for thread in self._threads:
            thread.start()
        for thread in self._threads:
            thread.join()

    def _get_version_download(self, version, url):
        try:
            # Establece un tiempo límite de 10 segundos
            print(f"GET {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if ok
            soup = BeautifulSoup(response.text, 'html.parser')
            download_box = soup.find(class_='well')
            download_link = download_box.find('a')['href']
            self._append_version(
                {'version': version, 'download': download_link})
        except requests.exceptions.Timeout:
            print(f"The requested {url} has exceed the timeout.")
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")

    def _get_command(self, jar_name):
        return f'java -jar {jar_name}'

    @staticmethod
    def get_name() -> str:
        """Returns manager name
        Returns:
            str: name
        """
        return "Spigot"
