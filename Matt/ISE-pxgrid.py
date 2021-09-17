import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def create_user():
    url = 'https://192.168.128.2:8910/pxgrid/control/AccountCreate'

    print(" ")
    new_name = input("Enter the new username: ")
    data = {
        "nodeName": new_name
    }

    request = requests.post(url, json=data, headers=headers, verify=False).json()

    new_creds = [request["userName"], request["password"]]

    return new_creds


def activate_and_check_account(creds):
    url = 'https://192.168.128.2:8910/pxgrid/control/AccountActivate'
    data = {}

    request = requests.post(url, headers=headers, json=data, verify=False, auth=(creds[0], creds[1])).json()

    return request['accountState']


# Create User
my_creds = create_user()

# Activate User
account_state = activate_and_check_account(my_creds)

# Check Status
while account_state == "PENDING":
    print(f'Account State: {account_state}')
    input("Please approve the request in ISE then press Enter...\n")
    account_state = activate_and_check_account(my_creds)

print(f"### Account Created ###\nUsername: {my_creds[0]}\nPassword: {my_creds[1]}")
