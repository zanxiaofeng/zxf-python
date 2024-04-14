from scapy.all import *
import ifaddr
import sys

DEFAULT_WINDOW_SIZE = 2052


# In order for this attack to work on Linux, we must
# use L3RawSocket, which under the hood sets up the socket
# to use the PF_INET "domain". This is required because of the
# way localhost works on Linux.
#
# See https://scapy.readthedocs.io/en/latest/troubleshooting.html#i-can-t-ping-127-0-0-1-scapy-does-not-work-with-127-0-0-1-or-on-the-loopback-interface for more details.
conf.L3socket = L3RawSocket

def find_iface(client_ip):
    local_ifaces = [
        adapter.name for adapter in ifaddr.get_adapters()
        if len([ip for ip in adapter.ips if ip.ip == client_ip]) > 0
    ]
    return local_ifaces[0]

def is_packet_on_tcp_conn(server_ip, server_port, client_ip):
    def f(p):
        if not p.haslayer(TCP):
            return False

        is_packet_tcp_client_to_server = p[IP].src == client_ip and p[IP].dst == server_ip and p[TCP].dport == server_port
        is_packet_tcp_server_to_client = p[IP].src == server_ip and p[IP].dst == client_ip and p[TCP].sport == server_port

        return is_packet_tcp_client_to_server or is_packet_tcp_server_to_client
    return f

def log_info(msg, params={}):
    formatted_params = " ".join([f"{k}={v}" for k, v in params.items()])
    print(f"{msg} {formatted_params}")

def log_packet(p):
    """This prints a big pile of debug information. We could make a prettier
    log function if we wanted."""
    return p.show()

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        log_info("Usage: python ./tcp-connection-monitor.py <client_ip> <server_ip> <server_port>")
        exit()
    
    client_ip = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])

    log_info("Starting sniff...")
    
    t = sniff(
        lfilter=is_packet_on_tcp_conn(server_ip, server_port, client_ip),
        iface=find_iface(client_ip),
        count=5000,
        prn=log_packet)
        
    log_info("Finished sniffing!")