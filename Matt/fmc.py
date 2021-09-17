#https://rich.readthedocs.io/en/latest/introduction.html

import fmc_variables
import requests
from rich import print
from rich.console import Console
from rich.table import Table
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
BASE_URL = "https://" + fmc_variables.FMC_IP + "/api/"

def get_token():
    username = fmc_variables.USERNAME
    password = fmc_variables.PASSWORD

    url = BASE_URL + 'fmc_platform/v1/auth/generatetoken'

    hdr = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        r = requests.post(url, headers=hdr, auth=(username, password), verify=False)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh); exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc); exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt); exit(1)
    except requests.exceptions.RequestException as err:
        print("Unknown Error:", err); exit(1)

    return r.headers['X-auth-access-token']


def get_server_info(t):
    url = BASE_URL + 'fmc_platform/v1/info/serverversion'

    hdr = {
        "X-auth-access-token": t
    }

    r = requests.get(url, headers=hdr, verify=False)
    if r.status_code != 200:
        print('There was an error')
        exit(1)

    response_json = r.json()
    server = response_json['items'][0]['serverVersion']
    geo = response_json['items'][0]['geoVersion']
    vdb = response_json['items'][0]['vdbVersion']
    sru = response_json['items'][0]['sruVersion']

    table = Table()
    table.add_column("Server Version", style="red")
    table.add_column("Geo Version", style="cyan")
    table.add_column("VDB Version", style="green")
    table.add_column("SRU Version", style="yellow")
    table.add_row(server, geo, vdb, sru)
    console = Console()
    console.print(table)


def list_devices(t):
    device_count = 0

    url = BASE_URL + 'fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords'

    hdr = {
        "X-auth-access-token": t
    }

    r = requests.get(url, headers=hdr, verify=False)
    if r.status_code != 200:
        print('There was an error')
        exit(1)

    response_json = r.json()

    if 'items' not in response_json:
        print("No Devices")
        return

    table = Table()
    table.add_column("Name", style="red")
    table.add_column("Type", style="cyan")
    table.add_column("UUID", style="green")

    for device in response_json['items']:
        table.add_row(device['name'], device['type'], device['id'])
        device_count += 1

    console = Console()
    console.print(table)

    return device_count


def add_device(t):
    url = BASE_URL + 'fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords'

    hdr = {
        "X-auth-access-token": t
    }

    ip = input("Enter the Device IP: ")
    name = input("Enter the Device Name: ")
    key = input("Enter the registration key: ")

    payload = {
        "name": name,
        "hostName": ip,
        "regKey": key,
        "type": "Device",
        "accessPolicy": {
            "id": "000C2955-709E-0ed3-0000-004294967299",
            "type": "AccessPolicy"
        }
    }

    r = requests.post(url, headers=hdr, json=payload, verify=False)

    print(f"Status Code: {r.status_code}")
    response_json = r.json()
    print(response_json)


def delete_device(t):
    devices = list_devices(t)
    if not devices:
        return

    hdr = {
        "X-auth-access-token": t
    }

    uuid = input("Enter the UUID of the device to be deleted: ")
    url = BASE_URL + 'fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords/' + uuid

    r = requests.delete(url, headers=hdr, verify=False)

    print(f"Status Code: {r.status_code}")
    response_json = r.json()
    print(response_json)


#Main Script
if __name__ == "__main__":
    print('\n' * 100 + 'Getting authentication token...')
    token = get_token()
    print(f"Token: {token}")
    print("Git Hub Test")

    while True:
        print("")
        print('1 - Print Server Info')
        print('2 - List Devices')
        print('3 - Register a new device')
        print('4 - Delete a device')
        choice = input('\nChoose an option or press enter to quit: ')

        if not choice:
            print('Exiting')
            exit(0)

        if choice == '1':
            get_server_info(token)
        if choice == '2':
            count = list_devices(token)
        if choice == '3':
            add_device(token)
        if choice == '4':
            delete_device(token)
