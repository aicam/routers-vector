# File organizations
lib directory contains all the functionalities need to be called
by main.py. It helps to keep code clean. <br>
```
parse_input_file.py it only works on the input routing information
router.py contains all the functions to create, update, edit routing vector
structures.py contains classes and variables used globally and their format
server.py contains functions and class needed to run UDP server and also send packet
```
Note: ROUTING_VECTOR is the only variable does not have
specification for the cost and nodes, it is a dictionary. Each
key represents the id of the node and value is a dictionary itself
with two keys: cost, vector. Cost shows the cost to the router and vector
indicates the next router.

# How system works
At the start of the server, routing table file is read and
parsed into a class named routing_table which only has information
of the host and its neighbors. This class is shared among other
modules to work with. The function with name generate_distance_vector_host
parse routing_table into the initial routing vector and store in
ROUTING_VECTOR. ROUTING_VECTOR is the main variable keeps distance and next hop of routers.
It only contains next server in routing and the overall cost to the node.
<br>
Note: we do not keep track of the whole path to the router, we only store next server in the path.

## How to synchronize based on new packets
Nodes are represented by IP and their ID is different among different servers,
in this regard, everytime a new packet arrives, we need to match
server IDs from other server to IDs in our server using routing_table.servers_ip
and then pass to update_distance_vector function to update ROUTING_VECTOR.