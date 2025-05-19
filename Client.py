import socket
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
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

            # Receive server's public RSA key
            server_public_pem = self.client_socket.recv(2048)
            server_public_key = serialization.load_pem_public_key(server_public_pem)

            # Generate Fernet key
            fernet_key = Fernet.generate_key()
            self.cipher_suite = Fernet(fernet_key)

            # Encrypt Fernet key with server's public RSA key
            encrypted_key = server_public_key.encrypt(
                fernet_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            self.client_socket.sendall(encrypted_key)

        except Exception as e:
            print(f"[Client] Connection error: {e}")

    def send_with_sync(self, command, payload=None):
        """Pulls DB, sends command, pushes DB"""
        try:
            # 1. Pull database from server
            self._send_command({"command": "fetch_database"})
            server_db = self._receive_response()
            if server_db:
                for table, table_data in server_db.items():
                    self.db.update_data(table, table_data)
                print("[Client] Synced DB from server before action")

            # 2. Perform action
            print("command: " +command)
            self._send_command({"command": command, "payload": payload})
            response = self._receive_response()
            print(f"[Client] Action response: {response}")

            # 3. Push updated DB back to server
            # full_data = {
            #     "Users": self.db.get_data("Users"),
            #     "Businesses": self.db.get_data("Businesses"),
            #     "Comments": self.db.get_data("Comments"),
            # }
            # self._send_command({"command": "update_database", "payload": full_data})
            # update_response = self._receive_response()
            # if update_response and update_response.get("status") == "success":
            #     print("[Client] Successfully pushed DB after action")
            # else:
            #     print("[Client] Failed to push DB after action")

            return response

        except Exception as e:
            print(f"[Client] Error in send_with_sync: {e}")
            return None

    def _send_command(self, message_dict):
        try:
            json_data = json.dumps(message_dict)
            encrypted = self.cipher_suite.encrypt(json_data.encode("utf-8"))
            self.client_socket.sendall(encrypted)
        except Exception as e:
            print(f"[Client] Error sending data: {e}")

    def _receive_response(self):
        try:
            encrypted_response = self.client_socket.recv(8192)
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

    def run_gui(self, client):
        """Initialize the GUI and start the main loop."""
        root = tk.Tk()
        HomePage(root, client)
        root.mainloop()


if __name__ == "__main__":
    client = Client('192.168.1.204')  # Change to your server IP
    client.connect()
    client.run_gui(client)
    client.close()
