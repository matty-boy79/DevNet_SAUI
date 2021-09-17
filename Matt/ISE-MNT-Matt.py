import requests

#url = 'https://192.168.128.2/admin/API/mnt/Session/ActiveList'
#url = 'https://192.168.128.2/admin/API/mnt/Session/UserName/matt'
#url = 'https://192.168.128.2/admin/API/mnt/Version'
url = 'https://192.168.128.2/admin/API/mnt/FailureReasons'

user = 'admin'
password = 'Applebikevirgin1!'
headers = {
    'Accept': 'application/xml'
}
request = requests.request('get', url, auth=(user, password), verify=False, headers=headers)

response = request.content

print(response)
