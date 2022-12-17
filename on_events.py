import socket
from select import select

check_to_read = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 5000))
server.listen()


def accept_connection(server):
    client, addr = server.accept()
    print('Connection from', addr)

    # Добавляем клиента в список для отслеживания:
    check_to_read.append(client)


def send_message(client):
    request = client.recv(2048)

    if request:
        client.send(f'Response message on {request.decode()}\n'.encode())
    else:
        client.close()


def event_loop():
    while True:

        """Тут мы ждем, когда select вернет нам списки объектов, которые мы отслеживаем. Как только наш список будет не 
        пустым, здесь сработает дебаг и мы увидим объекты сокетов. Далее идет обычная проверка на тип сокета и действия 
        в зависимости от ее результата."""
        ready_to_read, _, _ = select(check_to_read, [], [])  # to read, to write, errors

        for sock in ready_to_read:
            if sock is server:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    check_to_read.append(server)
    event_loop()
