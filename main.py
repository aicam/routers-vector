from lib.parse_input_file import read_file
from lib.server import UDPServerThread
from lib.structures import ROUTING_VECTOR, routing_table, NUM_RECEIVED_PACKETS, INFINITY
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

        if cmd.__contains__("update"):
            try:
                _, serverID1, serverID2, link_cost = cmd.split(' ')
                
                serverID1 = int(serverID1)
                serverID2 = int(serverID2)

                if link_cost == 'inf':
                    link_cost = INFINITY
                else:
                    link_cost = int(link_cost)

                UDP_server.send_update(serverID1, serverID2, link_cost)
                print(f"Server ID 1: {serverID1}\nServer ID 2: {serverID2}\nLink Cost:{link_cost}\n")

            except ValueError as e:
                print(f"Error: {e}")
                print("Command: update <server-ID1> <server-ID2> <Link Cost>")
                print()
            except Exception as e:
                print(f"An exception of type {type(e).__name__} occurred: {e}")
                print()

        if cmd.__contains__("disable"):
            try:
                _, serverID = cmd.split(' ')
                serverID = int(serverID)
                UDP_server.send_disable(serverID)
                print("Server Disabled")
                print(f"SERVER {serverID} HAS BEEN DISABLED")

            except ValueError as e:
                print(f"Error: {e}")
                print("Command: disable <server-ID1>")
                print()
            except Exception as e:
                print(f"An exception of type {type(e).__name__} occurred: {e}")
                print()