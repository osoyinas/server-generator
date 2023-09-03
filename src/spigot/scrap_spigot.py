import requests
import os
import sys
from bs4 import BeautifulSoup
import re
import json

URL = 'https://getbukkit.org/download/spigot'
JSON_FILE = 'src/spigot/data/spigot_versions.json'

def scrap_spigot(URL):
    print(f'Scraping {URL}')
    VERSION_LINKS = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_elements = soup.find_all(class_='download-pane')


    for element in download_elements:
        version = element.find('h2').text
        download_link_element = element.find('a', class_='btn-download')
        object = {'version': version, 'link':get_spigot_link(download_link_element['href'])}
        VERSION_LINKS.append(object)
    
    with open(JSON_FILE, 'w') as json_file:
        json.dump(VERSION_LINKS, json_file)    
    return VERSION_LINKS


def get_spigot_link(page_download_link):
    response = requests.get(page_download_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_box = soup.find(class_='well')
    download_link = download_box.find('a')['href']
    return download_link 


def get_spigot_versions():
    while not os.path.exists(JSON_FILE):
        scrap_spigot(URL)
    with open(JSON_FILE, 'r') as file:
        versions_dict = json.load(file)
        return list(map(lambda element: element['version'], versions_dict )) 


