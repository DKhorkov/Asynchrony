from time import sleep

"""Задача из вызывающего кода передавать на обработку данные в подгенератор через делегирующий генератор."""


def coroutine(generator_function):
    """Декоратор для функции генератора, чтобы его инициализировать."""
    def wrapper(*args, **kwargs):
        generator = generator_function(*args, **kwargs)
        generator.send(None)  # В первый раз при инициализации можно отправить в генератор только None
        return generator
    return wrapper


def subgen():
    """Подгенератор, читающий даныне из сокета, файла или еще откуда-то.
    Поскольку yield from содержит в себе инициализацию подегенератора, то нет смысла использовать инициализирующий
    декоратор @coroutine.

    Также необходимо создать механизм завершения работы подгенератора, иначе делегирующий генератор будет навечно
    заблокирован в ожидании результата от подгенератора в моменте result = yield from"""
    while True:
        try:
            message = yield
        except StopIteration:
            print('StopIteration Exception')
            break
        else:
            print('Here is the message', message)

    return 'Returned from subgen'


@coroutine
def delegator(generator_func):
    """Делегирующий генератор, транслирующий инфу из подгенератора.
    Конструкция yield from является упрощающей, также содержит в себе инициализацию подегенератора. Данная конструкция
    берет на себя отправку данных из делегирующего генератора в подгенератор, отправку исключений в подгенератор и прием
    результата из подгенератора, который можно обработать (Делегирующий генератор получает значение, которое
    возвращается с помощью return в подгенератора)."""
    result = yield from generator_func  # Также известен как await в других ЯП (ожидание заврешения работы подгенератора)
    print(result)


if __name__ == '__main__':
    subgen = subgen()
    delegator = delegator(subgen)

    # Вызывая next() для делегирующего генератора, мы будем получать значение из подгенератора:
    for i in range(11):
        delegator.send(i)
        sleep(1)
    delegator.throw(StopIteration)
