import requests
import json
import asyncio
import websockets
import ssl
import json
import ConfigHandler
import time
from datetime import datetime
import re

mattermostConfig = ConfigHandler.getMattermostConfig()

mattermostHookUrl = mattermostConfig['webhook']
user = mattermostConfig['user']
password = mattermostConfig['password']
mattermostApiUrl = mattermostConfig['api']
mattermostCommandChannel=mattermostConfig['commandChannel']

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

iconUrl = "http://icons.iconarchive.com/icons/google/noto-emoji-activities/256/52758-pool-8-ball-icon.png"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

token = None

latestEntry=None


def getPayloadBody(message):
    return {
        'channel': 'pool-ping',
        'username': 'pool-ping',
        'text': message,
        'icon_url': iconUrl
        }

def updateMattermostAvailable(available):
    state = "LEDIGT" if available == True else "UPPTAGET"
    body = getPayloadBody(state)
    response = requests.post(mattermostHookUrl, data=json.dumps(body), headers=headers)
    
def readLatestEntry():
    global mattermostCommandChannel
    
    headers = {'Authorization': 'Bearer '+ token }
    return requests.get(mattermostApiUrl + '/channels/'+mattermostCommandChannel+'/posts?per_page=1',  headers=headers).json()


def getCommand():
    global latestEntry
    cmd = None
        
    entry = readLatestEntry()
      
    postId = entry['order'][0]
    print('postID ' + str(postId))

    if not latestEntry or latestEntry['id'] != postId:
        post = entry['posts'][postId]   
        cmd = parseCommand(post['message'])
    
    latestEntry = entry
    return cmd
    
def parseCommand(cmd):
    if cmd.startswith('_'):
        actualCommand = {}
        params = cmd.split(',')
        actualCommand['command'] = params[0].replace('_','')
        params = params[1:]
        for x in params:
            p = x.split('=')
            actualCommand[p[0]] = p[1]
        return actualCommand
    
    return None
    

def getToken():
    global token
    global user
    global password
    if not token:
        response = requests.post(mattermostApiUrl + "/users/login",data=json.dumps({'login_id' : user, 'password': password}))

    token = response.headers['Token']
    
getMMToken()
cmd = getCommand()
print(cmd)