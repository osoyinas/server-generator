import requests
import os
import sys
from bs4 import BeautifulSoup
import re
import json
import threading

URL = 'https://files.minecraftforge.net/net/minecraftforge/forge/'
JSON_FILE = 'src/forge/data/forge_versions.json'

class ForgeManager:
    def __init__(self) -> None:
        self.URL = URL
        self.JSON_FILE = JSON_FILE
        self.versions = []
        self.versions_lock = threading.Lock()
        if not os.path.exists(JSON_FILE):
            self.scrap_forge()
            self._save_json()
        
        self._load_json()
    
    def get_forge_versions(self)->list:
        versions = list(map(lambda element: element['version'], self.versions ))
        
        def sort(version):
            return tuple(map(int, version.split('.')))

        return sorted(versions, key=sort, reverse=True)

    def scrap_forge(self):
        response = requests.get(self.URL)
        if response.status_code != 200:
            sys.exit(1)

        # parse html str to soup
        soup = BeautifulSoup(response.text, 'html.parser')

        #aux function, para filtrar los <a> que contienen la descarga y la version
        def versions_filter(tag):
            if tag.name == 'a' and tag.has_attr('href'):
                return re.match(r'index_(\d+\.\d+(\.\d+)?)\.html', tag['href']) 
            
        threads = []

        last_version = soup.find(class_='elem-active')
        last_version_thread = threading.Thread(target=self._get_version_download, args=(last_version.text, response.text))
        threads.append(last_version_thread)

        a_elements = soup.find_all(versions_filter)

        for element in a_elements:
            version_url = URL + element["href"]
            new_thread = threading.Thread(target=self._request_version_download, args=(element, version_url))
            threads.append(new_thread)
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def get_version(self,version:str)->dict:
        return next(filter(lambda d: d['version'] == version, self.versions), None)

    # Adquiere el lock para trabajar con la lista de las versiones
    def _append_version(self, version):
        with self.versions_lock:
            self.versions.append(version)

    def _save_json(self):
        with open(JSON_FILE, 'w' ) as json_file:
            json.dump(self.versions, json_file)

    def _load_json(self):
        with open(JSON_FILE, 'r' ) as json_file:
            self.versions = json.load(json_file)

    # Hace una peticion a la url (pagina de la version) y escrapea la pagina
    def _request_version_download(self, element, url):
        response = requests.get(url)
        print(f"GET {url}")
        self._get_version_download(element.text, response.text)

    
    # Scrapea el html para obtener los links de descarga de la version y las almacena concurrentemente en versions
    def _get_version_download(self, version, html)->dict:
        print(f'Scrapping {version}')
        version_dict = {'version': version}
        version_links = []

        soup = BeautifulSoup(html, 'html.parser')
        html_downloads = soup.find_all(class_='download')

        for download in html_downloads:
            download_title = download.find(class_='title').text.replace('\n', ' ').trim()
            download_elements = download.find_all(class_='link link-boosted')
            for download_element in download_elements:
                href = download_element.find('a')['href']
                version_dict[download_title] = href
                break


        self._append_version(version_dict)
        return version_dict



