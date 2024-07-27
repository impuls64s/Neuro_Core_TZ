import os 

import pytest
import requests
import requests_mock

from ..multithreaded_download import download_image, main
from ..utils import Counter


@pytest.fixture
def temp_folder(tmp_path):
    return tmp_path


@pytest.fixture
def mock_urls():
    return [
        'https://example.com/image1.jpg',
        'https://example.com/image2.png',
        'https://example.com/image3.gif'
    ]

def test_download_image_success(temp_folder, mock_urls):
    content_types = ['image/jpeg', 'image/png', 'image/gif']
    with requests_mock.Mocker() as mock:
        for n, url in enumerate(mock_urls):
            mock.get(
                url, status_code=200, content=b'fake image data',
                headers={'Content-Type': content_types[n]},
            )

        counter = Counter()
        total_urls = len(mock_urls)

        session = requests.Session()
        results = []

        for url in mock_urls:
            result = download_image(url, session, counter, total_urls, str(temp_folder))
            results.append(result)

        assert all(result is not None for result in results)
        assert len(os.listdir(temp_folder)) == total_urls


def test_download_image_failure(temp_folder):
    with requests_mock.Mocker() as mock:
        url = 'https://example.com/image.jpg'
        mock.get(url, status_code=404)

        counter = Counter()
        total_urls = 1
        session = requests.Session()

        result = download_image(url, session, counter, total_urls, str(temp_folder))
        assert result is None
        assert len(os.listdir(temp_folder)) == 0


def test_download_image_requests_exception(temp_folder):
    with requests_mock.Mocker() as mock:
        url = 'https://example.com/image.jpg'
        mock.get(url, exc=requests.exceptions.ConnectTimeout)

        counter = Counter()
        total_urls = 1
        session = requests.Session()

        result = download_image(url, session, counter, total_urls, str(temp_folder))
        assert result is None
        assert len(os.listdir(temp_folder)) == 0


def test_main_function(temp_folder, mock_urls):
    content_types = ['image/jpeg', 'image/png', 'image/gif']
    with requests_mock.Mocker() as mock:
        for n, url in enumerate(mock_urls):
            mock.get(
                url, status_code=200, content=b'fake image data',
                headers={'Content-Type': content_types[n]},
            )

        max_active_tasks = 5

        result = main(mock_urls, max_active_tasks, folder=str(temp_folder))

        assert len(result) == len(mock_urls)
        assert len(os.listdir(temp_folder)) == len(mock_urls)
