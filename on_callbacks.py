import selectors
import socket


selector = selectors.DefaultSelector()


def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen()

    # Регистрируем объект сервер-сокета для чтения и передали функцию, связанную с ним для выполнения:
    selector.register(server, selectors.EVENT_READ, accept_connection)


def accept_connection(server):
    client, addr = server.accept()
    print('Connection from', addr)

    # Регистрируем объект клиент-сокета для чтения и передали функцию, связанную с ним для выполнения:
    selector.register(client, selectors.EVENT_READ, send_message)


def send_message(client):
    request = client.recv(2048)

    if request:
        client.send(f'Response message on {request.decode()}\n'.encode())
    else:
        selector.unregister(client)
        client.close()


def event_loop():
    create_server()
    while True:

        """Тут мы ждем, когда selector вернет нам любой из объектов, которые мы отслеживаем и выполнит с ним функцию,
        которую мы передали ему в момент регистрации отслеживаемого объекта."""
        selector_keys = selector.select()  # returns (keys, events), поэтому нам нужен только первый элемент
        for key, _ in selector_keys:
            callback = key.data
            sock_obj = key.fileobj
            callback(sock_obj)


if __name__ == '__main__':
    event_loop()
