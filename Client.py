import socket
import json
import tkinter as tk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from HomePage import HomePage
from DButilities import DButilities

class Client:
    def __init__(self, host='192.168.1.204', port=65432):
        self.host = host
        self.port = port
        self.sock = None
        self.cipher = None
        self.db = DButilities()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        # 1) Receive server's RSA public key (PEM)
        pem = b""
        while True:
            chunk = self.sock.recv(1024)
            pem += chunk
            if b"-----END PUBLIC KEY-----" in pem:
                break

        public_key = serialization.load_pem_public_key(pem)

        # 2) Generate a fresh Fernet key
        fernet_key = Fernet.generate_key()
        self.cipher = Fernet(fernet_key)

        # 3) Encrypt the Fernet key with the server's RSA public key
        encrypted_key = public_key.encrypt(
            fernet_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 4) Send the encrypted Fernet key
        self.sock.sendall(encrypted_key)

        # 5) Pull initial database
        self.pull_database()
        print("[Client] Secure session established and DB pulled.")

    def send(self, msg: dict):
        data = json.dumps(msg).encode()
        encrypted = self.cipher.encrypt(data)
        self.sock.sendall(encrypted)

    def receive(self):
        encrypted = self.sock.recv(8192)
        data = self.cipher.decrypt(encrypted)
        return json.loads(data.decode())

    def pull_database(self):
        self.send({"command": "fetch_database"})
        db = self.receive()
        for table, content in db.items():
            self.db.update_data(table, content)

    def push_database(self):
        full = {
            "Users":     self.db.get_data("Users"),
            "Businesses":self.db.get_data("Businesses"),
            "Comments":  self.db.get_data("Comments"),
        }
        self.send({"command": "update_database", "payload": full})
        resp = self.receive()
        print("[Client] Push DB:", resp.get("status"))

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except: pass
        self.sock.close()

    def run_gui(self):
        root = tk.Tk()
        HomePage(root)
        root.mainloop()

if __name__ == "__main__":
    client = Client('192.168.1.204', 65432)
    client.connect()
    client.run_gui()
    client.push_database()
    client.close()
