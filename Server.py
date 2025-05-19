import socket
import threading
import json

from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import DButilities as DB
from Business import Business
from Comment import Comment

class Server:
    def __init__(self, host='192.168.1.204', port=65432):
        self.host = host
        self.port = port
        self.db = DB.DButilities()

        # Generate RSA key pair
        self._priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self._pub = self._priv.public_key()

        # Prepare listening socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"[Server] Listening on {self.host}:{self.port}")

    def handle_client(self, conn, addr):
        try:
            # 1) Send RSA public key (PEM) immediately
            pub_pem = self._pub.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            conn.sendall(pub_pem)

            # 2) Receive the encrypted Fernet key from client
            enc_key = conn.recv(512)  # size ok for one RSA-encrypted block

            # 3) Decrypt with RSA private key
            fernet_key = self._priv.decrypt(
                enc_key,
                padding.OAEP(
                    mgf=padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            cipher = Fernet(fernet_key)
            print(f"[Server] Secure session established with {addr}")

            # 4) Now handle encrypted JSON messages
            while True:
                blob = conn.recv(8192)
                if not blob:
                    break

                try:
                    request = json.loads(cipher.decrypt(blob).decode())
                    response = self.route(request)
                    conn.sendall(cipher.encrypt(json.dumps(response).encode()))
                except Exception as e:
                    err = {"error": str(e)}
                    conn.sendall(cipher.encrypt(json.dumps(err).encode()))

        finally:
            conn.close()
            print(f"[Server] Connection closed: {addr}")

    def route(self, data):
        cmd = data.get("command")
        pl  = data.get("payload")

        if cmd == "signup":
            users_data = self.db.get_data("Users")
            if any(u["username"] == pl["username"] for u in users_data.values()):
                return {"status": "fail", "message": "Username exists"}
            uid = str(len(users_data)+1)
            users_data[uid] = {"id":uid, **pl, "businesses":[]}
            print(users_data)
            self.db.update_data(name="Users", data=users_data)
            return {"status":"success"}

        if cmd == "login":
            users = self.db.get_data("Users")
            for u in users.values():
                if u["username"]==pl["username"] and u["password"]==pl["password"]:
                    return {"status":"success","id":u["id"]}
            return {"status":"fail"}

        if cmd == "get_businesses":
            return self.db.get_data("Businesses")

        if cmd == "add_business":
            bs = self.db.get_data("Businesses")
            bid = str(len(bs)+1)
            bs[bid] = {"id":bid, **pl, "comments":[]}
            self.db.update_data("Businesses", bs)
            # link to user
            us = self.db.get_data("Users")
            us[pl["owner_id"]]["businesses"].append(pl["name"])
            self.db.update_data("Users", us)
            return {"status":"success"}

        if cmd == "remove_business":
            bs = self.db.get_data("Businesses")
            cm = self.db.get_data("Comments")
            us = self.db.get_data("Users")
            name, oid = pl["name"], pl["owner_id"]
            to_del = next((k for k,v in bs.items() if v["name"]==name and v["owner_id"]==oid), None)
            if to_del:
                del bs[to_del]; self.db.update_data("Businesses", bs)
                for cid,v in list(cm.items()):
                    if v["business_id"]==to_del:
                        del cm[cid]
                self.db.update_data("Comments", cm)
                us[oid]["businesses"].remove(name)
                self.db.update_data("Users", us)
                return {"status":"success"}
            return {"status":"fail","message":"Not found"}

        if cmd == "add_comment":
            cm = self.db.get_data("Comments")
            cid = str(len(cm)+1)
            cm[cid] = {"id":cid, **pl}
            self.db.update_data("Comments", cm)
            # attach to business
            bs = self.db.get_data("Businesses")
            bs[pl["business_id"]]["comments"].append(cid)
            self.db.update_data("Businesses", bs)
            return {"status":"success"}

        if cmd == "get_comments":
            return self.db.get_data("Comments")

        if cmd == "fetch_database":
            return {
                "Users": self.db.get_data("Users"),
                "Businesses": self.db.get_data("Businesses"),
                "Comments": self.db.get_data("Comments")
            }

        if cmd == "update_database":
            self.db.update_data(name=pl["name"], data=pl["data"])
            return {"status":"success"}

        return {"status":"unknown command"}

    def start(self):
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    Server().start()
