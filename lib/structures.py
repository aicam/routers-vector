from typing import List

class ServerIPs:
    id: int
    ip: str
    port: int

    def __init__(self, line: str):
        line_s = line.split(" ")
        server_id = int(line_s[0])
        server_ip = line_s[1]
        server_port = int(line_s[2])
        self.port = server_port
        self.ip = server_ip
        self.id = server_id

class Distances:
    id1: int
    id2: int
    distance: int

    def __init__(self, line: str):
        line_s = line.split(" ")
        self.id1 = int(line_s[0])
        self.id2 = int(line_s[1])
        self.distance = int(line_s[2])

class RoutingTable:
    self_ip: str
    self_ip: str
    self_port: int
    num_servers: int
    num_neighbors: int
    servers_ip: List[ServerIPs]
    distances: List[Distances]

    def __init__(self):
        self.servers_ip = []
        self.distances = []

    def display(self):
        print("Host IP: ", self.self_ip)
        print("Host port: ", self.self_port)
        print("Number of servers: ", self.num_servers)
        print("Number of neighbors: ", self.num_neighbors)
        print("List of neighbor servers IDs, IP, ports")
        for s in self.servers_ip:
            print(f"ID: {s.id} - IP: {s.ip} - Port: {s.port}")
        print("List of neighbor servers ID and distance")
        for s in self.distances:
            print(f"ID 1: {s.id1} - ID 2: {s.id2} - distance: {s.distance}")