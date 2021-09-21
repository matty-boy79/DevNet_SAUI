import sw_variables
import requests
import json
from rich import print
from rich.console import Console
from rich.table import Table
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
BASE_URL = "https://" + sw_variables.SW_IP + "/"

def get_token(session):
    url = BASE_URL + "token/v2/authenticate"

    payload = {
        "username": sw_variables.USERNAME,
        "password": sw_variables.PASSWORD
    }

    session.post(url, data=payload, verify=False)


def get_tenants(session):
    url = BASE_URL + "sw-reporting/v1/tenants"

    tenant_id = session.get(url, verify=False).json()['data'][0]['id']
    return tenant_id


def get_tags(session, t):
    url = BASE_URL + "smc-configuration/rest/v1/tenants/" + str(t) + "/tags"
    r = session.get(url, verify=False)

    print(r.json())


def create_tag(session, t):
    url = BASE_URL + "smc-configuration/rest/v1/tenants/" + str(t) + "/tags"

    payload = {
        "name": "matt1",
        "location": "INSIDE",
        "ranges": ["192.168.1.1"],
        "parentId": 1
    }

    r = session.post(url, data=payload, verify=False)

    print(r.status_code)


if __name__ == "__main__":
    #Use a session to keep track of the authc cookie
    api_session = requests.Session()

    #Get authenticated
    get_token(api_session)

    #Get our tenant ID
    tenant = get_tenants(api_session)

    #Get all tags
    get_tags(api_session, tenant)

    #Create a new tag
    create_tag(api_session, tenant)
