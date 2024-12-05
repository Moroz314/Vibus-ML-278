from scapy.all import *
from scapy.packet import Packet


def process_packet(packet: Packet):
    if packet.haslayer(TCP):
        if packet[Ether].src == "victim_ip":
                if Raw in packet:
                    try:
                        data = packet[Raw].load.decode('utf-8')
                        data = json.loads(data)
                        print(data)
                    except:
                        print(packet[Raw].load)





cap = sniff(prn=process_packet)

