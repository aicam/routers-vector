import threading

from lib.parse_input_file import read_file
from lib.server import UDPServerThread
from lib.structures import ROUTING_VECTOR, routing_table
from lib.router import generate_distance_vector_host, update_cmd, disable_cmd
import time

def send_packet_interval(func, interval: int):
    while True:
        time.sleep(interval)
        func()

if __name__ == "__main__":
    # cmd = input("Enter server command to start server: ")

    # cmd_s = cmd.split(" ")
    top, interval = "routing.txt", 200

    read_file(top)
    routing_table.display()
    generate_distance_vector_host()
    print()

    UDP_server = UDPServerThread(routing_table.self_ip, routing_table.self_port)
    UDP_server.start()
    time.sleep(0.4)

    # Send update packet every interval
    interval_thread = threading.Thread(target=send_packet_interval, args=(UDP_server.send_packet, interval))
    interval_thread.daemon = True  # Set as a daemon thread
    interval_thread.start()

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
        if cmd.__contains__("update"):
            update_cmd(cmd)
            UDP_server.send_packet()
        if cmd.__contains__("disable"):
            disable_cmd(cmd, UDP_server.send_packet)
        if cmd == "crash":
            for i in range(2, routing_table.num_servers):
                disable_cmd("disable " + str(i), UDP_server.send_packet)
            exit()