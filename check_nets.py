import ipaddress
import pathlib
import socket

# Place all files in the same directory as the python script.
# Each file should contain one network per line. Single IPs will be converted to /32
# Place the list of known neworks in a text file name "known_ips.txt"
# Place the list of networks to check in "check_ips.txt"


# Output files will be "not_found.txt" and "found.txt"

script_dir = pathlib.Path(__file__).parent


def process_ip(ip_address):
    address = ip_address.strip()
    return ipaddress.IPv4Network(address, strict=False)

known_networks = []
networks_to_check = []

with open(script_dir / "known_ips.txt") as csvfile:
    current_ips_file = csvfile.readlines()
    for ip_address in current_ips_file:
        known_networks.append(process_ip(ip_address))


with open(script_dir / "check_ips.txt") as csvfile:
    check_ips_file = csvfile.readlines()
    for ip_address in check_ips_file:
        networks_to_check.append(process_ip(ip_address))


not_found = []
found = []
for network_to_check in networks_to_check:
    is_found = False
    while not is_found:
        for known_network in known_networks:
            if network_to_check.subnet_of(known_network):
                found.append({'network': network_to_check, 'found_in': known_network})
                is_found = True
                break
        break
    if not is_found:
        not_found.append(network_to_check)
        
    

with open(script_dir / "found.txt", "w") as outfile:
    for found_item in found:
        found = str(found_item['network'])
        found_in = str(found_item['found_in'])
        outfile.write(f"{found} in {found_in}\n")

with open(script_dir / "not_found.txt", "w") as outfile:
    for network in not_found:
        not_found = str(network)
        outfile.write(f"{not_found}\n")

