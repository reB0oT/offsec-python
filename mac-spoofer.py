#!/usr/bin/env python3

import subprocess
import argparse
import re


def args_parse():
    # Create an instance of ArgumentParser Class
    parser = argparse.ArgumentParser(prog="mac-spoofer.py",description="MAC address spoofer",epilog="Enjoy !\n")

    parser.add_argument('-i','--interface',required=True,dest="network_interface",help="Target network interface")
    parser.add_argument('-a','--address',required=True,dest="mac_address",help="MAC address to spoof")

    return parser.parse_args()

def check_interface_arg(network_interface):
    interface = subprocess.run(f"ip link show {network_interface} | grep '{network_interface}'", shell=True, capture_output=True, text=True) 
    if interface.stdout:
        return True
    else:
        print(f"[-] Network interface {network_interface} does not exist")
        return False

def check_address_arg(mac_address):
    match_mac_format = re.search(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address) 
    if match_mac_format:
        return True
    else:
        print(f"[-] {mac_address} is not a suitable MAC address format")
        return False


def get_mac_address(network_interface):
    check_cmd_return = subprocess.run(f"ip link show {network_interface} | grep 'ether'", shell=True, capture_output=True, text=True)
    # checking returned object stdout parameter is a string type :
    #print(type(cmd_return.stdout)) 
    
    # capturing MAC address with regex... TODO : try with cut or awk
    mac_address = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', check_cmd_return.stdout)
    return mac_address.group(0)


def spoof_mac_address(network_interface,mac_address):
    subprocess.run(f"ip link set dev {network_interface} down", shell=True)
    subprocess.run(f"ip link set dev {network_interface} address {mac_address}", shell=True)
    subprocess.run(f"ip link set dev {network_interface} up", shell=True)


def check_spoofing(network_interface, target_mac_address, initial_mac_address):
    current_mac_address = get_mac_address(network_interface)
    if current_mac_address == target_mac_address:
        print(f"[+] MAC address has been successfully changed to {target_mac_address}\n")
    elif current_mac_address == initial_mac_address:
        print(f"[-] Failed to spoof MAC address... MAC address is still {initial_mac_address}\n")
    else:
        print("[-] MAC address is neither target address nor initial address... Check the code !\n")


args = args_parse()
if check_interface_arg(args.network_interface) and check_address_arg(args.mac_address):
    initial_mac_address = get_mac_address(args.network_interface)
    print(f"[+] Trying to change MAC address for network interface {args.network_interface} from {initial_mac_address} to {args.mac_address}")
    spoof_mac_address(args.network_interface,args.mac_address)
    check_spoofing(args.network_interface, args.mac_address, initial_mac_address)
else:
    print("[-] Unable to proceed\n")








###########################################################################
##################### ifconfig legacy version #############################
###########################################################################

#subprocess.call(f"ifconfig {network_interface}", shell=True)

def legacy_spoof(network_interface,mac_address):
    mac_address_reset = "00:11:22:33:44:55"
    print(f"[+] Resetting MAC address for network interface {network_interface} to {mac_address_reset}")

    subprocess.call(f"ifconfig {network_interface} down", shell=True)
    subprocess.call(f"ifconfig {network_interface} hw ether {mac_address_reset}", shell=True)
    subprocess.call(f"ifconfig {network_interface} up", shell=True)

    subprocess.call(f"ifconfig {network_interface} | grep '{network_interface}\|ether", shell=True)




