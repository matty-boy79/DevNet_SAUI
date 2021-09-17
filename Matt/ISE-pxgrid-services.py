import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

creds = ['fart', 'YMHuD0nxDBfqp9l2']

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def check_services(my_creds):
    url = 'https://192.168.128.2:8910/pxgrid/control/ServiceLookup'
    data = {
            #"name": "com.cisco.ise.session"
            "name": "com.cisco.ise.config.anc"
    }

    request = requests.post(url, headers=headers, json=data, verify=False, auth=(creds[0], creds[1])).json()

    return request


services = check_services(creds)

print(services)

