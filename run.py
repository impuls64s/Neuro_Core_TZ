import asyncio

from async_download import main as async_download
from multithreaded_download import main as multithreaded_download
from utils import setup_logging


def main():
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
    setup_logging()
    max_active_tasks = 5
    result_async = asyncio.run(async_download(urls, max_active_tasks))  # Асинхронная загрузка
    result_multithreaded = multithreaded_download(urls, max_active_tasks)  # Мультипоточная загрузка


if __name__ == '__main__':
    main()
