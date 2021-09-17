import requests

amp_client_id = 'b15238bb3f7d9efa8fe4'
amp_api_key = '91c008ab-063c-4dc0-9fa4-7878e811ccaf'

def listEventTypes():
    url = 'https://api.eu.amp.cisco.com/v1/event_types'

    request = requests.get(url, auth=(amp_client_id, amp_api_key))
    response = request.json()

    print('{:^20} {:^15}'.format('ID', 'Name', 'Description'))

    for item in response["data"]:
        print('{:^20} {:<15}'.format(item['id'], item['name']))

if __name__ == '__main__':
    print("""
               Advanced Malware Protection (AMP) - Cloud

                    List Event Types :
                    """)

    listEventTypes()
