import asyncio
import os

import pytest
import aiohttp
from aioresponses import aioresponses

from ..async_download import download_image, main
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


@pytest.mark.asyncio
async def test_download_image_success(temp_folder, mock_urls):
    content_types = ['image/jpeg', 'image/png', 'image/gif']
    with aioresponses() as mock:
        for n, url in enumerate(mock_urls):
            mock.get(
                url, status=200, body=b'fake image data',
                headers={'Content-Type': content_types[n]},
            )

        counter = Counter()
        total_urls = len(mock_urls)
        semaphore = asyncio.Semaphore(5)
        session = aiohttp.ClientSession()
        results = []

        async def run_download(url):
            return await download_image(url, semaphore, session, counter, total_urls, str(temp_folder))

        tasks = [run_download(url) for url in mock_urls]
        results = await asyncio.gather(*tasks)

        assert all(result is not None for result in results)
        assert len(os.listdir(temp_folder)) == total_urls

    await session.close()


@pytest.mark.asyncio
async def test_download_image_failure(temp_folder):
    with aioresponses() as mock:
        url = 'https://example.com/image.jpg'
        mock.get(url, status=404)

        counter = Counter()
        total_urls = 1
        semaphore = asyncio.Semaphore(5)
        session = aiohttp.ClientSession()

        async def run_download(url):
            return await download_image(url, semaphore, session, counter, total_urls, str(temp_folder))

        result = await run_download(url)

        assert result is None
        assert len(os.listdir(temp_folder)) == 0

    await session.close()


@pytest.mark.asyncio
async def test_download_image_aiohttp_exception(temp_folder):
    with aioresponses() as mock:
        url = 'https://example.com/image.jpg'
        mock.get(url, exception=aiohttp.ClientError("Connection error"))

        counter = Counter()
        total_urls = 1
        semaphore = asyncio.Semaphore(5)
        session = aiohttp.ClientSession()

        async def run_download(url):
            return await download_image(url, semaphore, session, counter, total_urls, str(temp_folder))

        result = await run_download(url)

        assert result is None
        assert len(os.listdir(temp_folder)) == 0

    await session.close()


@pytest.mark.asyncio
async def test_main_function(temp_folder, mock_urls):
    with aioresponses() as mock:
        for url in mock_urls:
            mock.get(
                url, status=200, body=b'fake image data',
                headers={'Content-Type': 'image/jpeg'},
            )

        max_active_tasks = 5

        result = await main(mock_urls, max_active_tasks, folder=str(temp_folder))

        assert len(result) == len(mock_urls)
        assert len(os.listdir(temp_folder)) == len(mock_urls)
