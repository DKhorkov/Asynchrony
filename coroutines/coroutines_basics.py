def coroutine(generator_function):
    """Декоратор для функции генератора, чтобы его инициализировать."""
    def wrapper(*args, **kwargs):
        generator = generator_function(*args, **kwargs)
        generator.send(None)  # В первый раз при инициализации можно отправить в генератор только None
        return generator
    return wrapper


@coroutine
def average():
    count = 0
    amount = 0
    average_value = None

    while True:
        try:
            """Тут мы через метод gen_obj.send() отправляем данные в генератор. При инициализации отправляется None. 
            После этого генератор останавливается на этом месте. При следующей отправке (логика как с next(gen_obj) )
            мы передадим число в переменную x, произойдет вычисление нового среднего арифметического и его возврат нам
            из генератора. Можно также передавать исключения через gen_obj.throw()."""
            x = yield average_value
        except StopIteration as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break
        else:
            count += 1
            amount += x
            average_value = round(amount / count, 2)

    return f'average after Exceptions is {average_value}'
