### async_download.py - асинхронное скачивание изображений.

Этот модуль предоставляет функциональность для асинхронного скачивания изображений из списка URL-адресов. С указанием ограничения максимального количества одновременных задач. Папка для загурзки настраивается опционально, передав аргумент `folder='new_downloads/`. Пример:

```python
urls = [
    'https://cdn.pixabay.com/photo/2017/06/04/23/57/stem-2372543_640.png',
    'https://hips.hearstapps.com/redbook/assets/17/35/1504024434-lionlead.jpg',
]
max_active_tasks = 5
result = asyncio.run(main(urls, max_active_tasks))
```

### multithreaded_download.py - многопоточное скачивание изображений.
Этот модуль предоставляет функциональность для многопоточного скачивания изображений из списка URL-адресов. С указанием ограничения максимального количества одновременных потоков. Папка для загурзки настраивается опционально, передав аргумент `folder='new_downloads/`. Пример:

```python
urls = [
    'https://cdn.pixabay.com/photo/2017/06/04/23/57/stem-2372543_640.png',
    'https://hips.hearstapps.com/redbook/assets/17/35/1504024434-lionlead.jpg',
]
max_active_tasks = 5
result = main(urls, max_active_tasks)
```


### run.py - модуль  позволяющий переключаться между типами скачивания.

### Install

```sh
    git clone git@github.com:impuls64s/Neuro_Core_TZ.git
    cd Neuro_Core_TZ
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    export PYTHONPATH=$(pwd)

    pytets # Запуск тестов
```
