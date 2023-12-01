from . import structures as struct
from .structures import routing_table
def read_file(file):
    '''
    Read the routing table file
    :param file: path to the routing table
    :return: routing table class
    '''
    f = open(file, 'r', encoding='utf-8')
    lines = [l.replace("\n", "") for l in f.readlines()]
    routing_table.num_servers = int(lines[0])
    routing_table.num_neighbors = int(lines[1])
    for i in range(2, routing_table.num_neighbors + 3):
        routing_table.servers_ip.append(struct.ServerIPs(lines[i]))
    for i in range(routing_table.num_neighbors + 3, (2 * routing_table.num_neighbors) + 3):
        if lines == 'infinity':
            lines = float('inf')
        routing_table.distances.append(struct.Distances(lines[i]))
    self_host = [s for s in routing_table.servers_ip if s.id == 1][0]
    routing_table.self_ip = self_host.ip
    routing_table.self_port = self_host.port
    return routing_table