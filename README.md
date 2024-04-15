
# VLANs Information Extractor

This script extracts the VLANs information from the SDN > ACI table, and uses it to replace the `vlanId` in the Technology > VLANs table. It generates a CSV file with the following columns:

- hostname
- siteName
- vlanName
- vlanId
- status
- stdStatus

## Prerequisites

- Python 3.8 or higher
- IP Fabric platform with API access
- Python package: `ipfabric`

## Installation

1. Clone this repository or download the `vlans.py` script.
2. Install the required Python package:

```bash
pip install ipfabric
```

## How to Use

1. Copy the `.env.sample` file and rename it to `.env`:

    ```bash
    cp .env.sample .env
    ```

2. Open the `.env` file and set the following environment variables:

    - `IPF_URL`: Your IP Fabric platform URL
    - `IPF_TOKEN`: Your IP Fabric API token
    - `IPF_VERIFY`: (optional) Set to "True" to verify the SSL certificate. Default is "False".
    - `REPORT_OUTPUT`: (optional) Path to the output CSV file. Default is "vlan_report.csv".

3. Run the script:

```bash
python vlans.py
```

## Output

The script will generate a CSV file with the VLANs information. The file will be saved to the path specified in the `REPORT_OUTPUT` environment variable.
