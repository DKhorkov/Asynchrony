import requests
import asyncio
import aiohttp
from time import time


# Синхронное выполнение:

def get_picture(url):
    """Функция принимает ЮРЛ и возвращает объект ответа от сервера."""
    response = requests.get(url, allow_redirects=True)
    return response


def write_picture_to_file(response):
    """Функция принимает объект ответа и записывает его содержимое в файл."""
    filename = response.url.split('/')[-1]
    with open(f'images/{filename}', 'wb') as picture:
        picture.write(response.content)


def main():
    start = time()

    url = 'https://loremflickr.com/320/340'
    for i in range(10):
        write_picture_to_file(get_picture(url))

    end = time() - start
    print('Sync', end)


# Асинхронное выполнение:

async def fetch_content(url, session):
    """Создаем сессию, поскольку все запросы лучше делать через созданную сессию согласно документации aiohttp.
    С сессиями обычно работают через контекстный менеджер, поэтому async with. Все объекты, которые мы получаем являются
    асинхронным, поэтому необходимо использовать await."""

    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()  # Данный метод возвращает бинарные данные (картинку).

        """Обычно смешивать синхронный код с асинхронным внутри - плохая идея."""
        write_picture_to_file_async(data)


async def async_main():

    url = 'https://loremflickr.com/320/340'
    tasks = []

    """Создаем объект сессии и с помощью него заполняем список асинхронных задач"""
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(fetch_content(url, session))
            tasks.append(task)

        """Поскольку gather принимает распакованную последовательность, то передаем tasks со звездочкой 
        (его распакует)"""
        await asyncio.gather(*tasks)


def write_picture_to_file_async(data):
    """Функция синхронная, поскольку asyncio не предоставляет возможности для асинхронной работы с файлами."""
    filename = 'file-{}.jpeg'.format(int(time() * 1000))
    with open(f'images/{filename}', 'wb') as picture:
        picture.write(data)


if __name__ == '__main__':
    main()
    start = time()
    asyncio.run(async_main())
    print('Async', time() - start)
