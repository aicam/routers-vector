from . import structures as struct
from .structures import routing_table, INFINITY

def generate_distance_vector_host():
    '''
    This function updates the ROUTING_VECTOR based on host neighbours information, it is called when an update happen
    and on the beginning
    :param r_t: host RoutingTable
    :return: No return, just update the ROUTING_VECTOR
    '''
    for dst_id in range(1, routing_table.num_servers + 1):
        cost = 0
        vec = 0

        if dst_id == 1:
            cost = 0
            vec = 1
            struct.ROUTING_VECTOR.update({dst_id: {'cost': cost, 'vector': vec}})
            continue

        neighbor = [s for s in routing_table.distances if s.id2 == dst_id]
        if len(neighbor) == 0:
            cost = INFINITY
            vec = dst_id
        else:
            neighbor = neighbor[0]
            cost = neighbor.distance
            vec = dst_id
        struct.ROUTING_VECTOR.update({dst_id: {'cost': cost, 'vector': vec}})

def update_distance_vector(d_v: dict, node_id: int):
    '''
    This function is called after a new packet received from another node
    Note: incoming packet should be parsed into a dictionary with key = node_id in our routing table and value = cost
    :param d_v: dictionary of distances of the sending node to other nodes
    :param node_id: id of the node sent this packet (it should be found using IP address of the sender) 
    It will update the routing vector
    '''
    distance_from_node = struct.ROUTING_VECTOR[node_id]['cost']
    if distance_from_node > d_v[1]:
        distance_from_node = d_v[1]

    for dst_id in range(1, routing_table.num_servers + 1):

        if dst_id == 1:
            ## Cost to host is always 0
            continue

        if dst_id == node_id:
                continue

        if d_v[dst_id] + distance_from_node < struct.ROUTING_VECTOR[dst_id]['cost']:
            struct.ROUTING_VECTOR[dst_id]['cost'] = d_v[dst_id] + distance_from_node
            struct.ROUTING_VECTOR[dst_id]['vector'] = node_id
