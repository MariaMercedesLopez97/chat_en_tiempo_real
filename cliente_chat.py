import socket
import threading

# Configuración del cliente
HOST = '127.0.0.1'  # Dirección del servidor
PORT = 12345        # Puerto del servidor

# Crear un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Solicitar el nombre de usuario
username = input("Ingresa tu nombre de usuario: ")
client_socket.send(username.encode('utf-8'))

def receive_messages():
    """Función para recibir mensajes del servidor."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"\n{message.decode('utf-8')}")
            else:
                print("El servidor se ha cerrado.")
                break
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

# Crear un hilo para recibir mensajes
threading.Thread(target=receive_messages, daemon=True).start()

print(f"{username} se ha conectado al chat.")

while True:
    message = input()
    if message.lower() == 'exit':
        print("Desconectando...")
        client_socket.close()
        break
    # Enviar el mensaje sin duplicar el nombre de usuario
    full_message = f"{message}"  # Solo el contenido del mensaje
    client_socket.send(full_message.encode('utf-8'))
