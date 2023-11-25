import socket
import threading


class UDPServerThread:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True  # Set as a daemon thread

    def start_server(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP address and port
        sock.bind((self.ip, self.port))

        print(f"UDP server is running on {self.ip}:{self.port}...")

        while True:
            # Listen for incoming messages
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes

            print(f"Received message: {data.decode()} from {addr}")


    def start(self):
        self.server_thread.start()  # Start the server thread

    def stop(self):
        # You can implement any cleanup logic here if needed
        pass