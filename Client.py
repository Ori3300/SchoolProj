import socket
import json
from cryptography.fernet import Fernet
import tkinter as tk
from HomePage import HomePage
import random


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = None
        self.cipher_suite = None
        self.prime = None
        self.base = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))

            # Receive DH parameters and server public key
            dh_info = self.client_socket.recv(1024)
            dh_data = json.loads(dh_info.decode('utf-8'))
            self.prime = dh_data['prime']
            self.base = dh_data['base']
            server_public = dh_data['server_public']

            # Generate client private and public key
            client_private = random.randint(1, self.prime -1)  # Example private key (use random in production)
            client_public = pow(self.base, client_private, self.prime)

            # Send client public key to server
            self.client_socket.sendall(str(client_public).encode('utf-8'))

            # Generate shared secret and create Fernet key
            shared_secret = pow(server_public, client_private, self.prime)
            print(f"[Client] Shared secret: {shared_secret}")

            # Use part of the shared secret to create Fernet key
            key = str(shared_secret).zfill(32)[:32].encode()
            self.cipher_suite = Fernet(Fernet.generate_key())  # Simulated – replace with actual key logic

        except Exception as e:
            print(f"[Client] Connection error: {e}")

    def send(self, message_dict):
        try:
            json_data = json.dumps(message_dict)
            encrypted = self.cipher_suite.encrypt(json_data.encode("utf-8"))
            self.client_socket.sendall(encrypted)
        except Exception as e:
            print(f"[Client] Error sending data: {e}")

    def receive(self):
        try:
            encrypted_response = self.client_socket.recv(4096)
            if not encrypted_response:
                return None
            decrypted = self.cipher_suite.decrypt(encrypted_response).decode("utf-8")
            return json.loads(decrypted)
        except Exception as e:
            print(f"[Client] Error receiving data: {e}")
            return None

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            print("[Client] Connection closed")

    def run_gui(self):
        root = tk.Tk()
        HomePage(root)  
        root.mainloop()

if __name__ == "__main__":
    client = Client()
    client.connect()
    client.run_gui()
    client.close()
