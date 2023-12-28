import socket
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 55555

# Crear un socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lista para almacenar conexiones de clientes
clients = []
usernames = []

# Función para manejar las conexiones de los clientes
def handle_client(client):
    while True:
        try:
            # Recibir mensaje del cliente
            message = client.recv(1024).decode('utf-8')
            
            # Obtener el nombre de usuario del remitente
            index = clients.index(client)
            username = usernames[index]

            # Enviar mensaje a todos los clientes con el nombre de usuario
            broadcast(f'{username}: {message}')
        except:
            # Eliminar cliente si hay algún problema
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} se ha desconectado.')
            usernames.remove(username)
            break
        
# Función para enviar mensajes a todos los clientes
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            # Eliminar cliente si hay algún problema
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} se ha desconectado.')
            usernames.remove(username)
            break

# Función para aceptar conexiones de clientes
def accept_connections():
    while True:
        client, address = server.accept()
        print(f'Conexión establecida con {str(address)}')

        # Solicitar nombre de usuario
        client.send('NICK'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        # Agregar cliente y nombre de usuario a las listas
        usernames.append(username)
        clients.append(client)

        # Anunciar la conexión del nuevo cliente a todos los clientes
        broadcast(f'{username} se ha unido al chat.')

        # Enviar mensaje de bienvenida al nuevo cliente
        client.send('Conectado al servidor. ¡Bienvenido!'.encode('utf-8'))

        # Iniciar un hilo para manejar las comunicaciones del cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    print("Servidor iniciado.")
    accept_connections()
