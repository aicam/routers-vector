from lib.parse_input_file import read_file
from lib.server import UDPServerThread

if __name__ == "__main__":
    cmd = input("Enter server command to start server: ")

    cmd_s = cmd.split(" ")
    top, interval = cmd_s[2], int(cmd_s[4])

    r_t = read_file(top)
    r_t.display()

    UDP_server = UDPServerThread(r_t.self_ip, r_t.self_port)
    UDP_server.start_server()