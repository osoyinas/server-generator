"""
spigot_manager.py
"""
import sys
import os
import requests

from bs4 import BeautifulSoup

from src.manager import Manager

URL = 'https://minecraftversion.net/downloads/spigot/'
JSON_FILE = 'src/spigot/data/spigot_versions.json'


class SpigotManager(Manager):
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
            print(f"GET {self.url}")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # Check if ok

        except requests.exceptions.Timeout:
            print(f"The requested {self.url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred : {ex}")
            sys.exit(1)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('div', {'class': 'row', 'style': 'margin-bottom: 5%;'})

        for row in rows:
            version = row.find('h2').text
            download_link_element = row.find('a')
            url = download_link_element['href']
            self.versions.append({'version':version, 'download': url})


    @staticmethod
    def get_name() -> str:
        """Returns manager name

        Returns:
            str: name
        """
        return "Spigot"
