#https://rich.readthedocs.io/en/latest/introduction.html

import ftd_variables
import requests
from rich import print
from rich.console import Console
from rich.table import Table
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
BASE_URL = "https://" + ftd_variables.FTD_IP + "/api/fdm/v5/"

def get_token():
    username = ftd_variables.USERNAME
    password = ftd_variables.PASSWORD

    url = BASE_URL + 'fdm/token'

    payload = {
    "grant_type": "password",
    "username": username,
    "password": password
    }

    try:
        r = requests.post(url, json=payload, verify=False)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh); exit(1)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc); exit(1)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt); exit(1)
    except requests.exceptions.RequestException as err:
        print("Unknown Error:", err); exit(1)

    response = r.json()
    t = response['access_token']
    return t


def list_zones(t):
    url = BASE_URL + 'object/securityzones'

    hdr = {
        'Authorization': 'Bearer ' + t
    }

    r = requests.get(url, headers=hdr, verify=False)
    response_json = r.json()
    print(response_json)

    table = Table()
    table.add_column("Name", style="red")
    table.add_column("Description", style="red")
    table.add_column("Mode", style="green")
    table.add_column("UUID", style="yellow")

    for zone in response_json['items']:
        table.add_row(zone['name'], zone['description'], zone['mode'], zone['id'])

    console = Console()
    console.print(table)


def add_zone(t):
    url = BASE_URL + 'object/securityzones'

    hdr = {
        'Authorization': 'Bearer ' + t
    }

    zone_name = input("Enter Zone Name: ")

    payload = {
        "type": "securityzone",
        "mode": "ROUTED",
        "name": zone_name
    }

    r = requests.post(url, headers=hdr, json=payload, verify=False)
    response_json = r.json()
    print(response_json)


def delete_zone(t):
    list_zones(t)

    hdr = {
        'Authorization': 'Bearer ' + t
    }

    zone_to_delete = input('Enter UUID of zone to delete: ')

    url = BASE_URL + 'object/securityzones/' + zone_to_delete

    r = requests.delete(url, headers=hdr, verify=False)


def deploy(t):
    url = BASE_URL + 'operational/deploy'

    hdr = {
        'Authorization': 'Bearer ' + t
    }

    r = requests.post(url, headers=hdr, verify=False)
    response_json = r.json()
    print(response_json)


#Main Script
if __name__ == "__main__":
    print('\n' * 100 + 'Getting authentication token...')
    token = get_token()
    print(f"Token: {token}")

    while True:
        print("")
        print('1 - Get Security Zones')
        print('2 - Add Zone')
        print('3 - Delete Zone')
        print('4 - Deploy')
        choice = input('\nChoose an option or press enter to quit: ')

        if not choice:
            print('Exiting')
            exit(0)

        if choice == '1':
            list_zones(token)
        if choice == '2':
            add_zone(token)
        if choice == '3':
            delete_zone(token)
        if choice == '4':
            deploy(token)
