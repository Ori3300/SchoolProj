import socket
import threading
from cryptography.fernet import Fernet

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher = Fernet(key)

# Function to handle client communication
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    try:
        # Send the Fernet key to the client
        client_socket.send(key)
        print(f"[KEY SENT] Encryption key sent to {client_address}")

        while True:
            # Receive encrypted message from the client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"[DISCONNECTED] {client_address} disconnected.")
                break  # Client disconnected
            
            # Decrypt the message
            message = cipher.decrypt(encrypted_message).decode('utf-8')
            print(f"[{client_address}] {message}")

            # Encrypt and send the response back to the client
            response = cipher.encrypt(f"Server received: {message}".encode('utf-8'))
            client_socket.send(response)
    except Exception as e:
        print(f"[ERROR] {client_address}: {e}")
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
        print(f"[CONNECTED] {client_address} connected.")
        # Start a new thread for each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
