"""
This module provides functionality to download images asynchronously from a list of URLs.

It includes:
- The `download_image` function to download a single image.
- The `main` function to handle the download process for multiple URLs.
"""
import asyncio
import logging
import os
from typing import List, Optional

import aiofiles
import aiohttp

from utils import (Counter, content_type_to_extension, generate_unique_name,
                   load_credentials, setup_logging)


async def download_image(
    url: str,
    semaphore: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    counter: Counter,
    total_urls: int,
    folder: str,
) -> str:
    """
    Asynchronously downloads a file from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the file to download.
        semaphore (asyncio.Semaphore): Semaphore to limit the number of concurrent tasks.
        session (aiohttp.ClientSession): Aiohttp session to make HTTP requests.
        counter (Counter): Counter object for tracking the number of downloaded files.
        total_urls (int): Total number of URLs to download.
        folder (str): The folder where the downloaded file will be saved.

    Returns:
        str: The file path where the downloaded file is saved.
    """  # noqa: E501
    try:
        # Контролируем кол-во активных задач
        async with semaphore:
            # Выполняем GET запрос на URL
            async with session.get(url) as response:
                if response.status == 200:
                    # Получаем Content-Type из Headers
                    content_type = response.headers.get('Content-Type')
                    # Проверка валидного расширение (jpg, png, gif)
                    extension = content_type_to_extension.get(content_type)
                    if extension is None:
                        logging.warning(
                            f'Unsupported  Content-Type: {content_type} | URL => {url}',
                        )
                        return

                    # Генерируем уникальное имя для файла
                    unique_name = generate_unique_name()
                    file_path = os.path.join(folder, f'{unique_name}.{extension}')

                    # Сохраняем полученные данные в файл, не блокируя выполнение
                    data = await response.read()
                    async with aiofiles.open(file_path, 'wb') as file:
                        await file.write(data)

                    logging.info(
                        f'200 OK | {url[:30]}...{url[-10:]} => {file_path} | '
                        f'{counter} / {total_urls}',
                    )
                    # Увеличиваем счетчик
                    counter.increment()
                    return file_path
                else:
                    logging.warning(f'{response.status} ERORR | URL => {url}')
    except aiohttp.ClientError as error:
        logging.error(f'Aiohttp client error occurred for URL: {url}. Error: {error}')
    except Exception as error:
        logging.error(f'An unknown error occurred for URL: {url}. Error: {error}')


async def main(
    urls: list[str],
    max_active_tasks: int,
    cred_json_path: Optional[str] = 'credentials.json',
    folder: Optional[str] = 'downloads/',
) -> List[Optional[str]]:
    """
    Start the download process for the given list of URLs.

    Args:
        urls (list[str]): List of URLs to download.
        max_active_tasks (int): Maximum number of concurrent tasks.
        cred_json_path (str, optional): Path to the credentials file. Defaults to 'credentials.json'.
        folder (str, optional): Folder to save downloaded files. Defaults to 'downloads/'.

    Returns:
        List[Optional[str]]: A list of file paths where the downloaded files are saved. If a file could not be downloaded, its entry in the list will be `None`.
    """  # noqa: E501
    logging.info(' Async Downloading '.center(80, '#'))

    # Проверяем наличие папки для загрузки файлов, если ее нет, то создаем
    if not os.path.exists(folder):
        os.makedirs(folder)

    counter = Counter()  # Счетчик для лога
    total_urls = len(urls)

    # Загружаем все креды для отправки запросов
    cred = load_credentials(cred_json_path)

    # Создаем ограничитель активных задач
    semaphore = asyncio.Semaphore(max_active_tasks)

    # Создаем сессию в Aiohttp для последующей отправки запросов
    async with aiohttp.ClientSession(headers=cred['headers']) as session:
        # Под каждую ссылку создаем задачу
        tasks = [
            download_image(url, semaphore, session, counter, total_urls, folder)
            for url in urls
        ]
        # Запускаем задачи параллельно
        result = await asyncio.gather(*tasks)

    logging.info('The script has finished its work'.center(80, '-'))
    return result


if __name__ == '__main__':
    setup_logging()
    max_active_tasks = 5
    urls = [
        'https://cdn.pixabay.com/photo/2017/06/04/23/57/stem-2372543_640.png',  # noqa: E50
        'https://docs.aiohttp.org/en/stable/',  # noqa: E501
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbhGz3EHmtHBkrjYLUhhTWcfZaJFT1h_4M2w&s',  # noqa: E501
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKRr-HtArLFdW-OnHtCsS-Gg9gYwwYQ08xQA&s',  # noqa: E501
        'https://hugh.cdn.rumble.cloud/s/z8/c/B/H/j/cBHja.caa-happyanimals212-rr8nk2.jpeg',  # noqa: E501
        'https://www.womansworld.com/wp-content/uploads/2019/12/39-funny-animal-memes-that-are-impawsible-not-to-laugh-at-01-17.jpg?w=640',  # noqa: E501
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRl2TQzoCaOsJGnRk7UUSMUjD7bOhV6qyCQ9Q&s',  # noqa: E501
        'https://hips.hearstapps.com/redbook/assets/17/35/1504024434-lionlead.jpg',  # noqa: E501
        'https://www.liveabout.com/thmb/F8TGD3J_sEVFQCXMr-lrAOZAW8k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/dog-funny-face-58b8ecd55f9b58af5c9bd15d.jpg',  # noqa: E501
        'https://mymodernmet.com/wp/wp-content/uploads/archive/5jlLAXGFyrZYC1du9Wxm_1082119659.jpeg',  # noqa: E501
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9FUr4VB-2UzG83w4CMGIk77ai4nn-MhKpKw&s',  # noqa: E501
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_QgCrFTnj74rZhAOtuHlpFMTyYOb0M8jtPA&s',  # noqa: E501
        'https://www.tutorialspoiddddnt.com/online_python_formatter.htm',  # noqa: E501
    ]
    asyncio.run(main(urls, max_active_tasks))
