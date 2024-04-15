"""
# Description
This script extracts the VLANs information from the SDN > ACI table, and use it to replace the vlanId in the Technology > VLANs table.
It will generate a CSV file with the following columns:
- hostname
- siteName
- vlanName
- vlanId
- status
- stdStatus

# How to use
1. Set the environment variables (in a .env file or in the shell):
- IPF_URL: IP Fabric URL
- IPF_TOKEN: IP Fabric API token
- IPF_VERIFY: (optional) Set to "True" to verify the SSL certificate
- REPORT_OUTPUT: (optional) Path to the output CSV file (default: vlan_report.csv)

2. Install the required packages
pip install ipfabric

3. Run the script
python vlans.py

# Example
IPF_URL=https://ipfabric.local IPF_TOKEN=xxxx REPORT_OUTPUT=vlan_report.csv python vlans.py

# Changelog
- 2024-04-15: First version of the script

"""
import csv
import os

from dotenv import load_dotenv, find_dotenv
from ipfabric import IPFClient

load_dotenv(find_dotenv(), override=True)


# Get the path to the script's directory
ipf_url = os.getenv("IPF_URL")
ipf_auth = os.getenv("IPF_TOKEN")
ipf_verify = eval(os.getenv("IPF_VERIFY", "False").title())
report_output = os.getenv("REPORT_OUTPUT", "vlan_report.csv")

# Create an IPFClient object
ipf = IPFClient(base_url=ipf_url, auth=ipf_auth, snapshot_id="$last", verify=ipf_verify)

# Get devices inventory, excluding AP
not_ap_devices_filter = {"devType": ["neq", "ap"]}
all_devices = ipf.inventory.devices.all(filters=not_ap_devices_filter)

# Extract Device Detail data in Technology > VLANs
all_vlans_columns = [
    "hostname",
    "siteName",
    "vlanName",
    "vlanId",
    "status",
    "stdStatus",
]
all_vlans = ipf.technology.vlans.device_detail.all(columns=all_vlans_columns)

# Extract VLAN data in SDN > ACI
all_aci_vlans = ipf.technology.sdn.aci_vlan.all()

# Replace the VlanID in the all_vlans, by the encapVlanId from the matching entry in all_aci_vlans
## Create a dictionary to map unique keys (hostname, vlanId) to encapVlanId
mapping = {
    (item["hostname"], item["vlanId"]): item["encapVlanId"] for item in all_aci_vlans
}  # if item['encapVlanId'] != 0}

## Replace the vlanId in all_vlans with the encapVlanId from the mapping
for item in all_vlans:
    key = (item["hostname"], item["vlanId"])
    if key in mapping:
        item["vlanId"] = mapping[key]

# Export the data to a CSV file
with open(report_output, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_vlans_columns)
    writer.writeheader()
    for item in all_vlans:
        writer.writerow(item)

print(f"Report saved to {report_output}")
