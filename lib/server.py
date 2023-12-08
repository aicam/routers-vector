import socket
import threading
from .structures import routing_table, ROUTING_VECTOR, ServerIPs
from .router import update_distance_vector

def generate_message():
    ## This function reads routing_table and parse it to the correct format for sending to other nodes
    ## Routing updates are sent using the General Message format. All routing updates are UDP unreliable
    ## The message format for the data part is: 
    message = {}
    # Number of update fields check if the routing vector has any changes
    num_entries = len(ROUTING_VECTOR)
    message['number_of_updates'] = num_entries
    # Server port
    message['server_port'] = routing_table.self_port
    # Server IP
    message['server_IP'] = routing_table.self_ip
    message['distance_vectors'] = []
    for vec in ROUTING_VECTOR.keys():
        info_server = [s for s in routing_table.servers_ip if s.id == vec][0]
        new_vector = {'ip': info_server.ip, 'port': info_server.port, 'distance': ROUTING_VECTOR[vec]['cost']}
        message['distance_vectors'].append(new_vector)

    return message

def generate_vector_update_dict(message):
    node_info = [s for s in routing_table.servers_ip if s.ip == message['server_IP'] and s.port == message['server_port']]
    d_v = {}
    node_id = 0
    if len(node_info) == 0:
        routing_table.num_servers += 1
        routing_table.servers_ip.append(ServerIPs(f"{routing_table.num_servers} {message['server_IP']} {message['server_port']}"))
        node_id = routing_table.num_servers
    else:
        node_info = node_info[0]
        node_id = node_info.id

        for vec in message['distance_vectors']:
            id = [s for s in routing_table.servers_ip if s.ip == vec['ip'] and s.port == vec['port']][0].id
            dst = vec['distance']
            d_v.update({id: dst})

    update_distance_vector(d_v, node_id)



class UDPServerThread:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True  # Set as a daemon thread
        self.packet_count = 0
        

    def start_server(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP address and port
        sock.bind((self.ip, self.port))

        print(f"UDP server is running on {self.ip}:{self.port}...")

        while True:
            # Listen for incoming messages
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            received_data = self.deserialize_data(data)
            print(f"RECIEVED A MESSAGE FROM SERVER {received_data['server_port']}")
            generate_vector_update_dict(received_data)
            self.packet_count += 1

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

        update_packet = generate_message()
        for n in routing_table.servers_ip[1:]:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
                client_socket.sendto(str(update_packet).encode('utf-8'),(n.ip,n.port))
