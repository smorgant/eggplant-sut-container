#!/usr/bin/python3
import os, sys, requests, json, logging, socket

os.system("echo 'Python Script starting'")

response = requests.request("GET", "http://169.254.170.2/v2/metadata/")

response = json.loads(response.text)
response = response['Containers']
response = response['Networks']
response = json.dumps(response)

os.system("echo '" + response + "'")



#Confirm that they all exist first before moving forward
if 'URL' not in os.environ:
        sys.exit("URL Env variable missing")
        print("URL Env variable missing")

if 'CLIENT_ID' not in os.environ:
        sys.exit("CLIENT_ID Env variable missing")

if 'CLIENT_SECRET' not in os.environ:
        sys.exit("CLIENT_SECRET Env variable missing")

if 'EXECUTION_ID' not in os.environ:
        sys.exit("EXECUTION_ID Env variable missing")

# Print all the Env Variables to be used
logging.info(os.environ.get('URL'))
logging.info(os.environ.get('CLIENT_ID'))
logging.info(os.environ.get('CLIENT_SECRET'))
logging.info(os.environ.get('EXECUTION_ID'))

#Set variables used for the script
sut_name = "SUTEXECUTION" + os.environ.get('EXECUTION_ID')
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

#Create a Request to get the DAI token
url = os.environ.get('URL') + "/auth/realms/eggplant/protocol/openid-connect/token"
payload='grant_type=client_credentials&client_id=' + os.environ.get('CLIENT_ID') + '&client_secret=' + os.environ.get('CLIENT_SECRET')
headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

response = json.loads(response.text)
token = response['access_token']
logging.info(response['access_token'])

#Get the list of all current SUTs
url = os.environ.get('URL') + "/sut_service/api/v1/suts"

payload={}
headers = {
        'Authorization': 'Bearer ' + token
}

response = requests.request("GET", url, headers=headers, data=payload)

suts = json.loads(response.text)

logging.info(suts)

for sut in suts['items']:
        if sut['name'] == sut_name:
                sys.exit("SUT name already exist")

#Create a new SUT
url = os.environ.get('URL') + "/sut_service/api/v1/suts"

payload = json.dumps({
  "name": sut_name,
  "enabled": True,
  "connections": [
    {
      "connection_type": "VNC",
      "host": ip_address,
      "port": 5900,
      "username": "",
      "scale_ratio": 1,
      "password": "1234"
    }
  ],
  "execution_environments": [
    "EPFEXECUTION" + os.environ.get('EXECUTION_ID')
  ]
})

headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

sut = json.loads(response.text)

print(sut)
