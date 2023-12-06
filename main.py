from lib.parse_input_file import read_file
from lib.server import UDPServerThread
from lib.structures import ROUTING_VECTOR, routing_table
from lib.router import generate_distance_vector_host
import time



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
            print("display SUCCESS")
            print(ROUTING_VECTOR)
        if cmd == 'step':
            print("step SUCCESS")
            UDP_server.send_packet()
        if cmd == 'packets':
            print("packets SUCCESS")
            print(UDP_server.packet_count)
            UDP_server.packet_count = 0
        if cmd == 'exit':
            exit()