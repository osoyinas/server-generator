"""
forge_manager.py
"""
import os
import sys
import re
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

from src.manager import Manager

URL = 'https://files.minecraftforge.net/net/minecraftforge/forge/'
JSON_FILE = 'src/forge/data/forge_versions.json'


class ForgeManager(Manager):
    """
    Inherits from Manager, scrap the versions from URL and load data in JSON_FILE
    """

    def __init__(self) -> None:
        super().__init__(url=URL, json_file=JSON_FILE)

    def _scrap(self):
        """Scraps forge main page and parse the returned html with beautiful soup

        Returns:
            _type_: none
        """
        try:
            response = requests.get(self._url, timeout=10)
            response.raise_for_status()  # Check if ok

        except requests.exceptions.Timeout:
            print(f"The requested {self._url} has exceed the timeout.")
            sys.exit(1)
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred.")

            sys.exit(1)

        # parse html str to soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # aux function, para filtrar los <a> que contienen la descarga y la version
        def versions_filter(tag):
            if tag.name == 'a' and tag.has_attr('href'):
                return re.match(r'index_(\d+\.\d+(\.\d+)?)\.html', tag['href'])
        a_elements = soup.find_all(versions_filter)

        with ThreadPoolExecutor(max_workers=5) as executor:
            last_version = soup.find(class_='elem-active')
            executor.submit(self._request_version_download,
                            last_version.text, response.text)

            for element in a_elements:
                version_url = URL + element["href"]
                executor.submit(self._request_version_download,
                                element, version_url)

    def _request_version_download(self, element, url):
        try:
            # Establece un tiempo límite de 10 segundos
            print(f"GET {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Check if ok
            self._get_version_download(element.text, response.text)

        except requests.exceptions.Timeout:
            print(f"The requested {url} has exceed the timeout.")
        except requests.exceptions.RequestException as ex:
            print(f"An error ocurred.")

    def _get_version_download(self, version, html) -> dict:
        version_dict = {'version': version}
        soup = BeautifulSoup(html, 'html.parser')
        html_downloads = soup.find_all(class_='download')

        for download in html_downloads:
            download_title = download.find(
                class_='title').text.replace('\n', ' ').strip()
            download_elements = download.find_all(class_='link link-boosted')
            for download_element in download_elements:
                adfocus_url = download_element.find('a')['href']
                url = adfocus_url.split('url=')[1]
                version_dict[download_title] = url

        self._append_version(version_dict)
        return version_dict

    def _get_command(self, jar_name):
        return f'java -jar {jar_name} --installServer'

    @staticmethod
    def get_name() -> str:
        """Returns manager name

        Returns:
            str: name
        """
        return "Forge"
