import asyncio


async def print_number():
    number = 1
    while True:
        print(number)
        number += 1
        await asyncio.sleep(1)  # необходимо вызвать yield from, поскольку это асинхронный генератор


async def print_time():
    count = 0
    while True:
        if count % 5 == 0:
            print('{} seconds passed'.format(count))
        count += 1
        await asyncio.sleep(1)



async def main():
    task_1 = asyncio.create_task(print_number())  # Создаем задание, которое будет выполняться
    task_2 = asyncio.create_task(print_time())

    await asyncio.gather(task_1, task_2)  # Дожидаемся результата из корутин с помощью gather()


if __name__ == '__main__':
    asyncio.run(main())