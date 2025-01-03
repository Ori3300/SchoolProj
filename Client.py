import socket
from cryptography.fernet import Fernet

def start_client(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server {host}:{port}")

    try:
        # Receive the Fernet key from the server
        key = client.recv(1024)
        cipher = Fernet(key)
        print(f"[KEY RECEIVED] Encryption key: {key.decode()}")

        while True:
            # Input message to send
            message = input("Enter message to send (type 'exit' to disconnect): ")
            if message.lower() == 'exit':
                break
            
            # Encrypt the message
            encrypted_message = cipher.encrypt(message.encode('utf-8'))
            client.send(encrypted_message)

            # Receive and decrypt the server's response
            encrypted_response = client.recv(1024)
            response = cipher.decrypt(encrypted_response).decode('utf-8')
            print(f"Server: {response}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
