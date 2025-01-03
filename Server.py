import socket
import threading

# Function to handle client communication
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client disconnected
            print(f"[{client_address}] {message}")

            # Echo the message back to the client
            client_socket.send(f"Server received: {message}".encode('utf-8'))
    except ConnectionResetError:
        print(f"[DISCONNECTED] {client_address} disconnected.")
    finally:
        client_socket.close()

# Main function to start the server
def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)  # Max backlog of connections
    print(f"[LISTENING] Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
