import requests

client_id = 'b15238bb3f7d9efa8fe4'
api_key = '91c008ab-063c-4dc0-9fa4-7878e811ccaf'

protocol = 'https://'
base_url = 'api.eu.amp.cisco.com/v1/'
endpoint = 'computers'

#url = f'{protocol}{client_id}:{api_key}@{base_url}{endpoint}'
#request = requests.get(url)

url = f'{protocol}{base_url}{endpoint}'
request = requests.get(url, auth=(client_id, api_key))

response = request.json()

for item in response['data']:
    print(item['hostname'])

