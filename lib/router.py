from .structures import routing_table, INFINITY, ROUTING_VECTOR

def disable_cmd(cmd, step_func):
    id = int(cmd.split(" ")[1])
    for (i, dst) in enumerate(routing_table.distances):
        if dst.id2 == id:
            routing_table.distances[i].distance = INFINITY
    generate_distance_vector_host()
    step_func()
    for (i, server) in enumerate(routing_table.servers_ip):
        if server.id == id:
            routing_table.servers_ip[i].closed = True

def update_cmd(cmd):
    cmd_s = cmd.split(" ")
    id1 = int(cmd_s[1])
    id2 = int(cmd_s[2])
    cost = float(cmd_s[3])
    for (i, distance) in enumerate(routing_table.distances):
        if id2 == distance.id2:
            routing_table.distances[i].distance = cost

    generate_distance_vector_host()

def generate_distance_vector_host():
    '''
    This function updates the ROUTING_VECTOR based on host neighbours information, it is called when an update happen
    and on the beginning
    :param r_t: host RoutingTable
    :return: No return, just update the ROUTING_VECTOR
    '''
    for dst_id in range(1, routing_table.num_servers + 1):

        if dst_id == 1:
            cost = 0
            vec = 1
            ROUTING_VECTOR.update({dst_id: {'cost': cost, 'vector': vec}})
            continue

        neighbor = [s for s in routing_table.distances if s.id2 == dst_id]
        neighbor = neighbor[0]

        cost = neighbor.distance
        vec = dst_id if cost != INFINITY else 0
        ROUTING_VECTOR.update({dst_id: {'cost': cost, 'vector': vec}})

def update_distance_vector(d_v: dict, node_id: int):
    '''
    This function is called after a new packet received from another node
    Note: incoming packet should be parsed into a dictionary with key = node_id in our routing table and value = cost
    :param d_v: dictionary of distances of the sending node to other nodes
    :param node_id: id of the node sent this packet (it should be found using IP address of the sender) 
    It will update the routing vector
    '''
    distance_from_node = d_v[node_id]
    ROUTING_VECTOR[node_id] = {'cost': distance_from_node, 'vector': node_id if distance_from_node != INFINITY else 0}
    for dst_id in range(2, routing_table.num_servers + 1):
        if dst_id == node_id:
            continue

        if d_v[dst_id] + distance_from_node < ROUTING_VECTOR[dst_id]['cost'] or ROUTING_VECTOR[dst_id]['vector'] == node_id:
            ROUTING_VECTOR[dst_id]['cost'] = d_v[dst_id] + distance_from_node
            ROUTING_VECTOR[dst_id]['vector'] = node_id

        if distance_from_node == INFINITY and ROUTING_VECTOR[dst_id]['vector'] == node_id:
            ROUTING_VECTOR[dst_id]['cost'] = INFINITY
            ROUTING_VECTOR[dst_id]['vector'] = 0
