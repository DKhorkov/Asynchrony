from time import sleep

"""Делегирующий генератор - это генератор, вызывающий другой генератор. Подгенератор - это генератор, вызываемый
делегирующим генератором."""


def subgen():
    """Подгенератор, читающий даныне из сокета, файла или еще откуда-то."""
    for i in range(10):
        yield i


def delegator(generator_func):
    """Делегирующий генератор, транслирующий инфу из подгенератора."""
    for j in generator_func:
        yield j


if __name__ == '__main__':
    subgen = subgen()
    delegator = delegator(subgen)

    # Вызывая next() для делегирующего генератора, мы будем получать значение из подгенератора:
    for i in range(11):
        print(next(delegator))
        sleep(1)

