from time import sleep

"""Задача из вызывающего кода передавать на обработку данные в подгенератор через делегирующий генератор."""


def coroutine(generator_function):
    """Декоратор для функции генератора, чтобы его инициализировать."""
    def wrapper(*args, **kwargs):
        generator = generator_function(*args, **kwargs)
        generator.send(None)  # В первый раз при инициализации можно отправить в генератор только None
        return generator
    return wrapper


class TestException(Exception):
    pass


@coroutine
def subgen():
    """Подгенератор, читающий даныне из сокета, файла или еще откуда-то."""
    while True:
        try:
            message = yield
        except TestException:
            print('Here is the test Exception')
        else:
            print('Here is the message', message)


@coroutine
def delegator(generator_func):
    """Делегирующий генератор, транслирующий инфу из подгенератора."""
    while True:
        try:
            data = yield
            generator_func.send(data)
        except Exception as e:
            generator_func.throw(e)


if __name__ == '__main__':
    subgen = subgen()
    delegator = delegator(subgen)

    # Вызывая next() для делегирующего генератора, мы будем получать значение из подгенератора:
    for i in range(11):
        delegator.send(i)
        sleep(1)
    delegator.throw(TestException)
