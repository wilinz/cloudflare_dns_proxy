# Cloudflare DNS Proxy Manager

[简体中文](readme_zh_CN.md)  

This Python script allows users to manage the proxy settings of DNS records within their Cloudflare account. Specifically, it provides functionality to enable or disable the proxy status of DNS records for a given domain.

## Prerequisites

Before running the script, ensure you have the following prerequisites:

- Python 3.x installed on your system.
- `requests` library installed in Python. You can install it using `pip install requests`.
- A valid Cloudflare API token with the necessary permissions to read and write DNS records.

## Configuration

1. Replace `'your_api_token'` with your actual Cloudflare API token.
2. Replace `'example.com'` with the domain you want to manage.

## Usage

To run the script, use the following command:

```bash
python manage_dns_proxy.py
```

When prompted, input whether you want to enable (`e`) or disable (`d`) the proxy for DNS records. The script will then perform the following actions:

- Retrieve a list of all zones in your Cloudflare account.
- Find the zone ID corresponding to your domain.
- Fetch the DNS records for that zone.
- Optionally save the proxied DNS records to a JSON file named `proxied_records.json`.
- Enable or disable the proxy based on your choice.

If a `proxied_records.json` file already exists, you will be asked whether to use it or to fetch fresh records from the Cloudflare API.

## File Descriptions

- `manage_dns_proxy.py`: The main Python script that interacts with the Cloudflare API.
- `proxied_records.json`: A JSON file that stores the DNS records with proxy enabled, which can be used to manage the proxy settings offline.

## Notes

- The script sets a TTL of 600 seconds when disabling the proxy and 1 second (automatic) when enabling it.
- It is important to ensure that the API token used has the appropriate permissions to avoid unauthorized errors.

## Disclaimer

Use this script at your own risk. Always ensure you have backups and understand the changes you are making to your DNS records.

## Support

For any issues or questions, please open an issue on the GitHub repository where this script is hosted.

## License

This script is released under the MIT License. See the `LICENSE` file in the repository for full details.