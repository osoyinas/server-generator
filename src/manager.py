"""
This class provides a basic structure and common functionality for managing version information 
and performing data scraping in Python.
Derived classes are expected to implement the _scrap method to customize data retrieval for 
specific purposes.
"""
from abc import ABC, abstractmethod
import json
import threading


class Manager(ABC):
    """Class to manage versions and scrapping
    """

    def __init__(self, url, json_file) -> None:
        self.url = url
        self.json_file = json_file
        self.versions = []
        self.threads = []
        self.versions_lock = threading.Lock()


    def get_versions(self) -> list:
        """Obtain a sorted list of the available versions

        Returns:
            list: ["1.12.2", "1.9.3"]
        """
        versions = list(map(lambda element: element['version'], self.versions))

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
        return next(filter(lambda d: d['version'] == version, self.versions), None)

    def _save_json(self):
        with open(self.json_file, 'w', encoding='utf-8') as json_file:
            json.dump(self.versions, json_file)

    def _load_json(self):
        with open(self.json_file, 'r', encoding='utf-8') as json_file:
            self.versions = json.load(json_file)

    def _append_version(self, version):
        """Appends the version safely to self.versions

        Args:
            version (dict): version dict
        """
        with self.versions_lock:
            self.versions.append(version)

    @abstractmethod
    def _scrap(self):
        """Abstract method which obtains data
        """