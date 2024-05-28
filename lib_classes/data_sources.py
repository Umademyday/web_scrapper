# lib_classes/data_sources.py

from abc import ABC, abstractmethod


class BaseDataSource(ABC):
    @abstractmethod
    def fetch(self):
        pass


class URLDataSource(BaseDataSource):
    def __init__(self, url):
        self.url = url

    def fetch(self):
        import requests
        response = requests.get(self.url)
        return response.content


class FileDataSource(BaseDataSource):
    def __init__(self, file_path):
        self.file_path = file_path

    def fetch(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
