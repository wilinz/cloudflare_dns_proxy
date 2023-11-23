import requests
import json
import os

# Cloudflare API credentials
api_token = 'your_api_token'
domain_name = 'example.com'  # Replace with your domain
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# API endpoints
base_url = 'https://api.cloudflare.com/client/v4'
zones_url = f'{base_url}/zones'

# Get the list of all zones
zones_response = requests.get(zones_url, headers=headers)
zones = zones_response.json()['result']

# Find the zone_id for the given domain
zone_id = None
for zone in zones:
    if zone['name'] == domain_name:
        zone_id = zone['id']
        break

if zone_id is None:
    print(f'Zone ID for domain {domain_name} not found.')
    exit()

# Now that we have the zone_id, we can proceed to get the DNS records
dns_records_url = f'{base_url}/zones/{zone_id}/dns_records'

# JSON file to store proxied records
json_filename = 'proxied_records.json'

# Ask the user what they want to do
action = input("Do you want to enable ('e') or disable ('d') the proxy? [e/d]: ").strip().lower()

# Get records from API and ask user if they want to save to file
def fetch_and_optionally_save_records():
    response = requests.get(dns_records_url, headers=headers)
    proxied_records = [record for record in response.json()['result'] if record['proxied']]

    # Ask the user if they want to save these records to a file
    save_to_file = input("Do you want to save these records to a file? [y/n]: ").strip().lower()
    if save_to_file == 'y':
        with open(json_filename, 'w') as file:
            json.dump(proxied_records, file, indent=4)
        print(f"Records saved to {json_filename}.")
    return proxied_records

if action == 'd':
    # Disable proxy
    if os.path.exists(json_filename):
        use_file = input(f"Do you want to use the existing '{json_filename}' file? [y/n]: ").strip().lower()
        if use_file == 'y':
            # Load records from file
            with open(json_filename, 'r') as file:
                proxied_records = json.load(file)
        else:
            proxied_records = fetch_and_optionally_save_records()
    else:
        proxied_records = fetch_and_optionally_save_records()

    # Disable proxy for each record
    for record in proxied_records:
        record_id = record['id']
        record_data = {
            'type': record['type'],
            'name': record['name'],
            'content': record['content'],
            'ttl': 600,
            'proxied': False
        }
        update_url = f'{dns_records_url}/{record_id}'
        update_response = requests.put(update_url, headers=headers, json=record_data)
        if update_response.status_code == 200:
            print(f'Successfully disabled proxy for {record["name"]}')
        else:
            print(f'Failed to update record {record["name"]}')
elif action == 'e':
    # Enable proxy
    if os.path.exists(json_filename):
        # Load records from file
        with open(json_filename, 'r') as file:
            dns_records = json.load(file)

        # Enable proxy for each record
        for record in dns_records:
            record_id = record['id']
            record_data = {
                'type': record['type'],
                'name': record['name'],
                'content': record['content'],
                'ttl': 1,  # TTL can be 1 for proxied records
                'proxied': True
            }
            update_url = f'{dns_records_url}/{record_id}'
            update_response = requests.put(update_url, headers=headers, json=record_data)
            if update_response.status_code == 200:
                print(f'Successfully enabled proxy for {record["name"]}')
            else:
                print(f'Failed to update record {record["name"]}')
    else:
        print(f"File '{json_filename}' does not exist. Cannot enable proxy without the file.")
else:
    print("Invalid action. Please enter 'e' to enable or 'd' to disable the proxy.")
