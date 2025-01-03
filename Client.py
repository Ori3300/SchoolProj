import socket

def start_client(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Connected to server {host}:{port}")

    try:
        while True:
            # Send a message to the server
            message = input("Enter message to send (type 'exit' to disconnect): ")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))

            # Receive and print the server's response
            response = client.recv(1024).decode('utf-8')
            print(f"Server: {response}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()
