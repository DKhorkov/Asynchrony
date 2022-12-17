"""Будет две функции, одна будет выводить числа от 0 до бесконечности, а другая раз в несколько секунд будет выводить
текущее время."""

import asyncio


@asyncio.coroutine
def print_number():
    number = 1
    while True:
        print(number)
        number += 1
        yield from asyncio.sleep(1)  # необходимо вызвать yield from, поскольку это асинхронный генератор


@asyncio.coroutine
def print_time():
    count = 0
    while True:
        if count % 5 == 0:
            print('{} seconds passed'.format(count))
        count += 1
        yield from asyncio.sleep(1)



@asyncio.coroutine
def main():
    task_1 = asyncio.ensure_future(print_number())  # Создаем объект будущего, где мы что-то получим из корутины
    task_2 = asyncio.ensure_future(print_time())

    yield from asyncio.gather(task_1, task_2)  # Дожидаемся результата из корутин с помощью gather()


# @asyncio.coroutine
    # def test():
    #     """Данные декоратор делает из функции генератор-корутину. А если функция уже является генератором, то
    #     декоратор ее же нам и вернет."""
    #     return 'test'
    #
    #
    # g = test()
    # next(g)


if __name__ == '__main__':
    # Создаем событийный цикл, который будет работать до полного завершения, после чего закрываем событийный цикл:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()