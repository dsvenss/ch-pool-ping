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
import Logger

from ScoreKeeper import ScoreKeeper
from PoolTableFinder import PoolTableFinder

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
    token = getToken()
    return {'Authorization': 'Bearer '+ token }

def updateMattermostAvailable(available):
    Logger.info('Posting availability: ' + str(available))
    state = "LEDIGT" if available == True else "UPPTAGET"
    data = getPayloadBody(state)
    response = requests.post(mattermostHookUrl, json=data, headers=headers)
    
def readLatestEntry():
    global mattermostCommandChannel    
    headers = getHeaders()
    return requests.get(mattermostApiUrl + '/channels/'+mattermostCommandChannel+'/posts?per_page=1',  headers=headers).json()

def getCommands():
    global latestEntry
    cmds = []
        
    entry = readLatestEntry()
      
    postId = entry['order'][0]
    Logger.info("Getting commands")
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
    
    
def postCroppedImage():
    
    poolFinder = PoolTableFinder()
    poolFinder.saveCroppedImage()
    
    postImage(ConfigHandler.getCroppedImagePath())

def postRawImage():
    postImage(ConfigHandler.getCurrentImagePath())

def postImage(path):
    response = uploadImage(path)
    imageId = getImageId(response)
    
    Logger.info("Posting image")
    headers = getHeaders()
    data = {'channel_id' : mattermostCommandChannel, 'message' : 'Pool table image', 'file_ids': [imageId]}
    requests.post(mattermostApiUrl + "/posts", json=data, headers=headers)

def postIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    ip = s.getsockname()[0]
    
    Logger.info("Posting IP")
    post(ip)
    
def postScore():
    score = str(ScoreKeeper.score)
    Logger.info("Posting score: " + score)
    post(score)
    
def post(msg):
    headers = getHeaders()
    data = {'channel_id' : mattermostCommandChannel, 'message' : msg}

    response = requests.post(mattermostApiUrl + "/posts", json=data, headers=headers)
    
def postLog():
    log = Logger.getLog()
    Logger.info("Posting log")
    post(log)
    
def getImageId(response):
    return response['file_infos'][0]['id']
    
def uploadImage(path):
    headers = getHeaders()
    
    Logger.info("Uploading image")
        
    f = open(path, 'rb')
    formData = {'files': f, 'channel_id' : (None, mattermostCommandChannel)}
    response = requests.post(mattermostApiUrl + "/files", files=formData, headers=headers)
    
    return response.json()

def getToken():
    global token
    global user
    global password
    if not token:
        data = {'login_id' : user, 'password': password}
        Logger.info("Getting token")
        response = requests.post(mattermostApiUrl + "/users/login",json=data)
        token = response.headers['Token']
    
    return token