import socket
import threading
from .structures import routing_table, ROUTING_VECTOR
def generate_message():
    ## This function reads routing_table and parse it to the correct format for sending to other nodes
    ## Routing updates are sent using the General Message format. All routing updates are UDP unreliable
    ## The message format for the data part is: 
    message = {}
    # Number of update fields check if the routing vector has any changes
    ## TODO add real updated entries
    num_entries = len(ROUTING_VECTOR)
    message['Number_of_updates'] = num_entries
    # Server port
    message['Server_port'] = routing_table.self_port
    # Server IP
    message['Server_IP'] = routing_table.self_ip
    # Server entry to reach itself wit hcost 0
    message['Server_IP_address_1'] = routing_table.self_ip
    message['Server_port_1'] = routing_table.self_port
    message['Server_ID1'] = "Cost 0"

    for i, (x ,y) in enumerate(zip(routing_table.servers_ip[1:],routing_table.distances),2):
        message['Server_IP_address_' + str(i)] = x.ip
        message['Server_port_' +str(i)] = x.port
        message['Server_ID' + str(i )] = "Cost " + str(y.distance)
    

    return message


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
            # Parse data to correct format for update_distance_vector function and pass it to
            print(f"Received message: {data.decode()} from {addr}")

            received_data = self.deserialize_data(data)

    def deserialize_data(self, data):
        # Convert the received string data to a dictionary
        decoded_data = data.decode('utf-8')
        received_data = eval(decoded_data)  # Use eval cautiously; it's suitable here since we control the format
        return received_data

    def start(self):
        self.server_thread.start()  # Start the server thread

    def stop(self):
        # You can implement any cleanup logic here if needed
        pass

    def send_packet(self):
        ## This function is called on "step" command to send messages to all servers in routing_table
        #

        for n in routing_table.servers_ip[1:]:
            update_packet = generate_message()
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                client_socket.sendto(str(update_packet).encode('utf-8'),('localhost',n.port))
