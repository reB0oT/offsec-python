#!/usr/bin/env python3

import scapy.all as scapy
import argparse

def args_parse():
    parser = argparse.ArgumentParser(prog="arp-scanner.py",description="ARP network scanner")
    parser.add_argument('-t', '--target',required=True,type=str,dest="target",help="Target address/network")
    return parser.parse_args()

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether() 
    broadcast.dst="ff:ff:ff:ff:ff:ff"
    arp_broadcast_request = broadcast/arp_request

    answered_packets = scapy.srp(arp_broadcast_request, timeout=1, verbose=False)[0] 
    
    hosts_up = []
    for element in answered_packets:
        hosts_up.append({"ip" : element[1].psrc, "mac" : element[1].hwsrc})
    return hosts_up

def print_targets(hosts_up):
    print("\nIP Address\t\tMAC Address\n-----------------------------------------")
    for host in hosts_up:
        print(host["ip"] + "\t\t" + host["mac"])
    print("\n")


target = args_parse()
hosts_up = scan(target.target)
print_targets(hosts_up)
