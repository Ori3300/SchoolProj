import socket
import json
import random
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import tkinter as tk
from HomePage import HomePage
from DButilities import DButilities

class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.client_socket = None
        self.cipher_suite = None
        self.db = DButilities()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))

            # Diffie-Hellman Key Exchange
            dh_info = self.client_socket.recv(1024)
            dh_data = json.loads(dh_info.decode('utf-8'))
            prime = dh_data['prime']
            base = dh_data['base']
            server_public = dh_data['server_public']

            client_private = random.randint(1, prime - 1)
            client_public = pow(base, client_private, prime)
            self.client_socket.sendall(str(client_public).encode('utf-8'))

            shared_secret = pow(server_public, client_private, prime)
            print(f"[Client] Shared secret: {shared_secret}")

            key = str(shared_secret).zfill(32)[:32].encode()
            fernet_key = urlsafe_b64encode(key)
            self.cipher_suite = Fernet(fernet_key)

            self.pull_database()

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
            encrypted_response = self.client_socket.recv(8192)
            if not encrypted_response:
                return None
            decrypted = self.cipher_suite.decrypt(encrypted_response).decode("utf-8")
            return json.loads(decrypted)
        except Exception as e:
            print(f"[Client] Error receiving data: {e}")
            return None

    def pull_database(self):
        self.send({"command": "fetch_database"})
        data = self.receive()
        if data:
            for table, table_data in data.items():
                self.db.update_data(table, table_data)
            print("[Client] Pulled database from server.")

    def push_database(self):
        full_data = {
            "Users": self.db.get_data("Users"),
            "Businesses": self.db.get_data("Businesses"),
            "Comments": self.db.get_data("Comments"),
        }
        self.send({"command": "update_database", "payload": full_data})
        response = self.receive()
        if response and response.get("status") == "success":
            print("[Client] Successfully pushed local DB to server.")
        else:
            print("[Client] Failed to push DB to server.")

    def close(self):
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            self.client_socket.close()
            print("[Client] Connection closed")

    def run_gui(self):
        root = tk.Tk()
        HomePage(root)
        root.mainloop()

if __name__ == "__main__":
    client = Client('192.168.2.35')  # Set to your server's IP
    client.connect()
    client.run_gui()
    client.push_database()
    client.close()
