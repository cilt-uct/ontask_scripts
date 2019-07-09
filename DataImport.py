import requests, json
from requests.auth import HTTPDigestAuth
import pandas

def Login():
    url = 'https://localhost:8000/auth/local/'

    payload = {
        'email':'email',
        'password':'password'
    }

    headers = {
        'Content-Type':'application/json'
    }

    data = json.dumps(payload)

    r = requests.post(url, data=data, verify=False, headers=headers)
    return r.text

def GetAllContainers(token):
    url = 'https://localhost:8000/administration/containers/'

    r = requests.get(url, verify=False, headers=GetHeader(token))
    return r.text

def UpdateContainerData():
    login_response = json.loads(Login())
    token = login_response['token']

    containers = json.loads(GetAllContainers(token))

    create_url = 'https://localhost:8000/datasource/'

    for container in containers:
        # import some data
        siteMembers = GetSiteMemberships(container['description'])
        df = pandas.DataFrame.from_records(siteMembers, index=[0])
        df.to_csv('memberships.csv')
        files = {'file': open('memberships.csv', 'rb')}
        payload = GetPayload(membership, container['id'])
        r = requests.post(create_url, data=payload, files=files, verify=False, headers=GetHeader(token))
        print(r.text)

def DoesDataSourceExist(token):
    url = 'https://localhost:8000/datasource/'
    r = requests.get(url, data=payload, files=files, verify=False, headers=GetHeader(token))


def VulaLogin():

    url = 'https://devslscle001.uct.ac.za/direct/session'

    body = {
        '_username':'user',
        '_password':'pass'
    }

    headers = {
        'Accept': "application/json",
        'Cache-Control': "no-cache"
    }

    r = requests.post(url, data=body, headers=headers)
    return r.text

def GetSiteMemberships(siteId):
    session = VulaLogin()
    url = 'https://devslscle001.uct.ac.za/direct/site/'+siteId+'/memberships?_validateSession=true&sakai.session='+session

    headers = {
        'Accept':'application/json',
        'Cache-Control': "no-cache"
    }

    r = requests.get(url, headers=headers)
    return r.text


def GetPayload(name, container):
    payload = {
        'name': name,
        'container': container,
        'payload': '{"connection":{"dbType":"csvTextFile","files":[{"name":"test_csv.csv","delimiter":","}]},"name":"Test"}',
    }

    return payload

def GetHeader(token):
    headers = {
        'Authorization': "Token " + token
    }

    return headers

UpdateContainerData()