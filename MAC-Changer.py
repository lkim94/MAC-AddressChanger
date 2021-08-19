#!/usr/bin/env python3

# Very simple Python program for changing the MAC address of a given network interface card.

# USAGE: python3 MAC-Changer.py -i <interface_name> -m <new_mac_address>

import argparse, subprocess, re

# Function for taking inputs such as the interface and the new MAC address to change to.
def get_args(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Specifies the interface to change its MAC address.")
    parser.add_argument("-m", "--mac", dest="mac", help="Specifies the new MAC address to assign.")
    values = parser.parse_args()
    while values.interface == None:
        values.interface = input("\n[!]ERROR: Please specify the interface to change it's MAC address: ")
    while values.mac == None:
        values.mac = input("\n[!]ERROR: Please specify the new MAC address to asssign: ")
    return values

# Function for chaning the MAC address.
def change_mac(interface, mac):
    print(f"\n[+] Changing the MAC address of {interface} to {mac}...")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

# Function for checking the result to see if the MAC address was changed successfully.
def check_results(interface, mac):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result)).group(0)
        current_mac = str(current_mac).upper()
        if current_mac == mac:
            print(f"\n[+] Successfully changed the MAC address of {interface} to {mac}")
            print(f"[+] Current MAC address: {current_mac}\n")
        else:
            print(f"\n[!] ERROR: Failed to change the MAC address of {interface} to {mac}")
            print(f"[=] Current MAC address: {current_mac}\n")
    except AttributeError:
        print("\n[!]ERROR: No MAC address found for the specified interface.\n")

#_______________________________________________________________________________________________________________________

values = get_args()
interface = values.interface
mac = values.mac

change_mac(interface, mac)
check_results(interface, mac)
