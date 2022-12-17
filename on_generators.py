import socket
from select import select
from queue import Queue

tasks = Queue()
to_read = {}
to_write = {}


def server_work():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen()

    while True:

        yield 'read', server  # Тут происходит остановка. Оставшаяся часть итерации пройдет после вызова gen_obj.next()

        client, addr = server.accept()  # read
        print('Connection from', addr)

        # Кладем в очередь клиентский соккет
        tasks.put(client_work(client))


def client_work(client):
    while True:

        yield 'read', client

        request = client.recv(2048)  # read

        if not request:
            break
        else:
            yield 'write', client

            client.send(f'Response message on {request.decode()}\n'.encode())  # write

    client.close()


def event_loop():

    """Функция принимает несколько значений, каждое из которых возвращает булево. Если хоть одно true, то any()
    вернет True. Поскольку мы работаем с циклом, нужно его всегда подкармливать. Если очередь задач пуста, то с помощью
    select() получаем готовые сокеты и добавляем связанный с сокетом генератор в очередь задач на выполнение, а также
    одновременно удаляем из списков на чтение/запись. Если очередь не пуста, то вызываем next() генератора, в котором
    производится действие над сокетами, а затем снова добавляем сокет и его генератор в список для чтения или записи."""
    while any([tasks, to_read, to_write]):

        while tasks.empty():
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.put(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.put(to_write.pop(sock))

        try:
            task = tasks.get()  # Тут хранится генератор.

            action, sock = next(task)
            if action == 'read':
                to_read[sock] = task
            elif action == 'write':
                to_write[sock] = task
        except StopIteration:
            print('End of iteration')


if __name__ == '__main__':
    tasks.put(server_work())
    event_loop()
