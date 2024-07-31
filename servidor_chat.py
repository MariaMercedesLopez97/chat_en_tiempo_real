import socket
import select

# Configuración del servidor
HOST = '127.0.0.1'  # Escucha en localhost
PORT = 12345        # Puerto del servidor

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Servidor de chat escuchando en {HOST}:{PORT}")

# Lista de sockets conectados y diccionario de usuarios
clients = []
usernames = {}

def broadcast(message, current_socket):
    """Enviar mensajes a todos los clientes excepto al que los envió."""
    for client in clients:
        if client != current_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error al enviar mensaje a {client}: {e}")
                client.close()
                clients.remove(client)

while True:
    # Esperar por eventos de I/O
    read_sockets, _, exception_sockets = select.select([server_socket] + clients, [], clients)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            # Un nuevo cliente se está conectando
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            # Leer el nombre de usuario
            username = client_socket.recv(1024).decode('utf-8')
            usernames[client_socket] = username
            print(f"Nuevo cliente conectado: {username} desde {client_address}")

            # Enviar notificación a todos los clientes de que un nuevo cliente se ha unido
            broadcast(f"{username} se ha unido al chat.".encode('utf-8'), client_socket)
        else:
            # Mensaje recibido de un cliente
            try:
                message = notified_socket.recv(1024)
                if not message:
                    raise Exception("Cliente desconectado")

                # Crear mensaje con el nombre de usuario
                username = usernames[notified_socket]
                full_message = f"{username}: {message.decode('utf-8')}".encode('utf-8')
                print(full_message.decode('utf-8'))
                broadcast(full_message, notified_socket)
            except Exception as e:
                print(f"Error: {e}")
                clients.remove(notified_socket)
                notified_socket.close()
                del usernames[notified_socket]

server_socket.close()
