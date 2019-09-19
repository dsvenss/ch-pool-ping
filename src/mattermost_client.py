import requests
import json
import asyncio
import websockets
import ssl
import json
import ConfigHandler
import time
from datetime import datetime 

mattermostConfig = ConfigHandler.getMattermostConfig()

mattermostHookUrl = mattermostConfig['webhook']
iconUrl = "http://icons.iconarchive.com/icons/google/noto-emoji-activities/256/52758-pool-8-ball-icon.png"
mattermostApiUrl = mattermostConfig['api']

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
token = None

latestCommand=None


def getPayloadBody(message):
    return {
        'channel': 'pool-ping',
        'username': 'pool-ping',
        'text': message,
        'icon_url': iconUrl
        }

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def updateMattermostAvailable(available):
    state = "LEDIGT" if available == True else "UPPTAGET"
    body = getPayloadBody(state)
    response = requests.post(mattermostHookUrl, data=json.dumps(body), headers=headers)
    
def readLatestCommand():
    headers = {'Authorization': 'Bearer '+ token }
    return requests.get(mattermostApiUrl + '/channels/1awbmkoaebgg7rq9osdpiowdrw/posts?per_page=1',  headers=headers).json()


def parseCommand():
    command = None
    postId = None
    post = None
    cmd = None
    global latestCommand
        
    command = readLatestCommand()
      
    postId = command['order'][0]
    print('postID ' + str(postId))

    if not latestCommand or latestCommand['id'] != postId
        post = command['posts'][postId]   
        cmd = post['message']
    
    latestCommand = command
    return cmd
    
def getMMToken():
    global token
    if not token:
        response = requests.post(mattermostApiUrl + "/users/login",data=json.dumps({'login_id' : mattermostConfig['user'], 'password':mattermostConfig['password']}))

    token = response.headers['Token']
    
getMMToken()
cmd = parseCommand()
print(str(cmd))