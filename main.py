from lib.parse_input_file import read_file
from lib.server import UDPServerThread
from lib.structures import ROUTING_VECTOR, routing_table, NUM_RECEIVED_PACKETS
from lib.router import generate_distance_vector_host
from lib.server import generate_message
import time
'''
    TODO:
    record all times packet received
    
'''

if __name__ == "__main__":
    cmd = input("Enter server command to start server: ")

    cmd_s = cmd.split(" ")
    top, interval = cmd_s[2], int(cmd_s[4])

    read_file(top)
    routing_table.display()
    generate_distance_vector_host()
    print()

    UDP_server = UDPServerThread(routing_table.self_ip, routing_table.self_port)
    UDP_server.start()
    time.sleep(0.4)

    print()

    while True:
        ## Commands come here
        cmd = input("Enter new command: \n")
        if cmd == 'display':
            print(ROUTING_VECTOR)
        if cmd == 'step':
            UDP_server.send_packet()
        if cmd == 'exit':
            exit()