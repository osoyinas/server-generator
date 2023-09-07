"""
This class provides a basic structure and common functionality for managing version information 
and performing data scraping in Python.
Derived classes are expected to implement the _scrap method to customize data retrieval for 
specific purposes.
"""
import sys
import os
import threading
from abc import ABC, abstractmethod
import json
import requests


class Manager(ABC):
    """Class to manage versions and scrapping
    """

    def __init__(self, url, json_file, server_path=os.getcwd()) -> None:
        self.set_server_path(server_path)
        self._url = url
        self._json_file = json_file
        self._versions = []
        self._threads = []
        self._picked_version = {}
        self._versions_lock = threading.Lock()

    def set_server_path(self, path):
        self.server_path = os.path.join(path, 'server')
        if not os.path.exists(self.server_path):
            os.mkdir(self.server_path)

    def get_versions(self) -> list:
        """Obtain a sorted list of the available versions

        Returns:
            list: ["1.12.2", "1.9.3"]
        """
        versions = list(
            map(lambda element: element['version'], self._versions))

        def sort(version):
            return tuple(map(int, version.split('.')))

        return sorted(versions, key=sort, reverse=True)

    def get_version_of(self, version: str) -> dict:
        """Returns a dict with the version and the available downloads.

        Args:
            version (str): ex: "1.12.2"

        Returns:
            dict: ex: "{version: "1.12.2", download: "https://link..."}"
        """
        return next(filter(lambda d: d['version'] == version, self._versions), None)

    def get_picked_version_downloads(self):
        """Returns the available downloads from the picked version

        Returns:
            _type_: _description_
        """
        keys = list(self._picked_version.keys())
        keys.remove('version')
        return keys

    def set_picked_version(self, version: str):
        """Sets the picked version

        Args:
            version (str): "1.12.2"

        Returns:
            _type_: {'version': '1.12.2', 'download': '....'}
        """
        self._picked_version = self.get_version_of(version)
        return self._picked_version

    def download_jar(self, url, jar_name):
        """Donwloads the file given by the url in the path

        Args:
            path (str): where the file will be storaged
            url (str): download url
        """
        jar_path = os.path.join(self.server_path, jar_name)
        print(f'Downloading {url} in {self.server_path}')
        try:
            response = requests.get(url=url, timeout=10)
            response.raise_for_status()
            with open(jar_path, 'wb') as jar_file:
                jar_file.write(response.content)
        except requests.exceptions.Timeout:
            print(f"The requested {url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred with {url}: {ex}")

    def init_server(self, download_picked):
        """Starts the server on the setted path

        Args:
            download_picked (str): download key, default='download'
        """
        jar_name = f"server-{self._picked_version['version']}.jar"
        self.download_jar(
            url=self._picked_version[download_picked], jar_name=jar_name)
        os.chdir(self.server_path)
        os.system(f'java -jar {jar_name} --installServer')

    def _save_json(self):
        with open(self._json_file, 'w', encoding='utf-8') as json_file:
            json.dump(self._versions, json_file)

    def _load_json(self):
        with open(self._json_file, 'r', encoding='utf-8') as json_file:
            self._versions = json.load(json_file)

    def _append_version(self, version):
        """Appends the version safely to self.versions

        Args:
            version (dict): version dict
        """
        with self._versions_lock:
            self._versions.append(version)

    @abstractmethod
    def _scrap(self):
        """Abstract method which obtains data
        """
