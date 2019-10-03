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
import socket
import Util

mattermostConfig = ConfigHandler.getMattermostConfig()

mattermostHookUrl = mattermostConfig['webhook']
user = mattermostConfig['user']
password = mattermostConfig['password']
mattermostApiUrl = mattermostConfig['api']
mattermostCommandChannel=mattermostConfig['commandChannel']
mattermostInfoChannel=mattermostConfig['infoChannel']

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

def getHeaders():
    global token
    return {'Authorization': 'Bearer '+ token }

def updateMattermostAvailable(available):
    Util.log('Posting availability: ', str(available))
    state = "LEDIGT" if available == True else "UPPTAGET"
    data = getPayloadBody(state)
    response = requests.post(mattermostHookUrl, json=data, headers=headers)
    
def readLatestEntry():
    global mattermostCommandChannel
    token = getToken()
    
    headers = getHeaders()
    return requests.get(mattermostApiUrl + '/channels/'+mattermostCommandChannel+'/posts?per_page=1',  headers=headers).json()


def getCommands():
    global latestEntry
    cmds = []
        
    entry = readLatestEntry()
      
    postId = entry['order'][0]
    Util.log("Getting commands")
    if not latestEntry or latestEntry['id'] != postId:
        post = entry['posts'][postId]   
        cmds = parseCommands(post['message'])
        latestEntry = entry['posts'][postId]
    
    return cmds
    
def parseCommands(cmd):
    commandList = []
    commands = cmd.splitlines()
    for command in commands:
        if command.startswith('_'):
            actualCommand = {}
            params = command.split(',')
            actualCommand['command'] = params[0].replace('_','')
            params = params[1:]
            for x in params:
                p = x.split('=')
                actualCommand[p[0]] = p[1]
            commandList.append(actualCommand)
    
    return commandList
    
    
def postImage():
    token = getToken()
    response = uploadImage()
    imageId = getImageId(response)
    
    Util.log("Posting image")
    headers = getHeaders()
    data = {'channel_id' : mattermostCommandChannel, 'message' : 'Pool table image', 'file_ids': [imageId]}
    requests.post(mattermostApiUrl + "/posts", json=data, headers=headers)
    
def postIP():
    token = getToken()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    ip = s.getsockname()[0]
    
    headers = getHeaders()
    data = {'channel_id' : mattermostCommandChannel, 'message' : ip}
    
    Util.log("Posting IP")
    response = requests.post(mattermostApiUrl + "/posts", json=data, headers=headers)
    print(response.content)
    
def getImageId(response):
    return response['file_infos'][0]['id']
    
def uploadImage():
    token = getToken()
    
    headers = getHeaders()
    f = open('current.jpg', 'rb')
    formData = {'files': f, 'channel_id' : (None, mattermostCommandChannel)}
    response = requests.post(mattermostApiUrl + "/files", files=formData, headers=headers)
    
    Util.log("Uploading image")
    return response.json()

def getToken():
    global token
    global user
    global password
    if not token:
        data = {'login_id' : user, 'password': password}
        Util.log("Getting token")
        response = requests.post(mattermostApiUrl + "/users/login",json=data)
        token = response.headers['Token']
    
    return token