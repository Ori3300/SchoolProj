import socket
import threading
import json
from cryptography.fernet import Fernet
import DButilities as DB
from Business import Business
from Comment import Comment
import random

class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.db = DB.DButilities()
        self.prime = 23
        self.base = 5
        print(f"Server started at {self.host}:{self.port}")

    def handle_client(self, client_socket, addr):
        try:
            # Diffie-Hellman key exchange
            server_private = random.randint(1, self.prime-1)  # Example private key (should be random in production)
            server_public = pow(self.base, server_private, self.prime)

            # Send DH parameters and server public key
            dh_info = json.dumps({
                'prime': self.prime,
                'base': self.base,
                'server_public': server_public
            }).encode('utf-8')
            client_socket.sendall(dh_info)

            # Receive client public key
            client_public = int(client_socket.recv(1024).decode('utf-8'))
            shared_secret = pow(client_public, server_private, self.prime)
            fernet_key = Fernet.generate_key()[:32]
            shared_key = Fernet(Fernet.generate_key())

            # Use part of the shared secret to generate a Fernet key
            key = str(shared_secret).zfill(32)[:32].encode()
            cipher = Fernet(Fernet.generate_key())  # Simulated - replace with derived key logic
            print(f"[Server] Shared secret with {addr}: {shared_secret}")

            while True:
                encrypted_data = client_socket.recv(8192)
                if not encrypted_data:
                    break

                try:
                    data = cipher.decrypt(encrypted_data).decode("utf-8")
                    data = json.loads(data)
                    response = self.route(data)
                    encrypted_response = cipher.encrypt(json.dumps(response).encode("utf-8"))
                    client_socket.sendall(encrypted_response)
                except Exception as e:
                    print(f"[Server] Error decrypting: {e}")
                    error = cipher.encrypt(json.dumps({"error": str(e)}).encode("utf-8"))
                    client_socket.sendall(error)

        finally:
            client_socket.close()

    def route(self, data):
        command = data.get("command")
        payload = data.get("payload")

        if command == "signup":
            users = self.db.get_data("Users")
            for user in users.values():
                if user['username'] == payload['username']:
                    return {"status": "fail", "message": "Username already exists."}
            user_id = str(len(users)+1)
            users[user_id] = {
                "id": user_id,
                "username": payload['username'],
                "password": payload['password'],
                "businesses": []
            }
            self.db.update_data("Users", users)
            return {"status": "success"}

        elif command == "login":
            users = self.db.get_data("Users")
            for user in users.values():
                if user['username'] == payload['username'] and user['password'] == payload['password']:
                    return {"status": "success", "id": user['id']}
            return {"status": "fail"}

        elif command == "add_business":
            businesses = self.db.get_data("Businesses")
            business_id = str(len(businesses) + 1)
            businesses[business_id] = {
                "id": business_id,
                "name": payload['name'],
                "category": payload['category'],
                "description": payload['description'],
                "location": payload['location'],
                "owner_name": payload['owner_name'],
                "owner_id": payload['owner_id'],
                "comments": []
            }
            self.db.update_data("Businesses", businesses)

            users = self.db.get_data("Users")
            users[payload['owner_id']]['businesses'].append(payload['name'])
            self.db.update_data("Users", users)

            return {"status": "success"}

        elif command == "remove_business":
            businesses = self.db.get_data("Businesses")
            comments = self.db.get_data("Comments")
            users = self.db.get_data("Users")
            name = payload['name']
            user_id = payload['owner_id']

            business_id = None
            for id, b in businesses.items():
                if b['name'] == name and b['owner_id'] == user_id:
                    business_id = id
                    break
            if business_id:
                del businesses[business_id]
                self.db.update_data("Businesses", businesses)

                for cid in list(comments):
                    if comments[cid]['business_id'] == name:
                        del comments[cid]
                self.db.update_data("Comments", comments)

                users[user_id]['businesses'].remove(name)
                self.db.update_data("Users", users)
                return {"status": "success"}
            return {"status": "fail", "message": "Business not found."}

        elif command == "get_businesses":
            return self.db.get_data("Businesses")

        elif command == "get_users":
            return self.db.get_data("Users")

        elif command == "get_comments":
            return self.db.get_data("Comments")

        elif command == "add_comment":
            comments = self.db.get_data("Comments")
            comment_id = str(len(comments)+1)
            comments[comment_id] = {
                "id": comment_id,
                "username": payload['username'],
                "content": payload['content'],
                "business_id": payload['business_id']
            }
            self.db.update_data("Comments", comments)

            businesses = self.db.get_data("Businesses")
            for id, b in businesses.items():
                if b['id'] == payload['business_id']:
                    b['comments'].append(comment_id)
                    break
            self.db.update_data("Businesses", businesses)

            return {"status": "success"}

        return {"status": "unknown command"}

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server = Server()
    server.start()