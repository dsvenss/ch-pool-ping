import requests
import ssl
import ConfigHandler
import socket

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

availableIconUrl = "https://previews.123rf.com/images/floralset/floralset1706/floralset170600119/80446026-billiard-green-pool-ball-with-number-6-snooker-transparent-background-vector-illustration-.jpg"
busyIconUrl = "https://previews.123rf.com/images/floralset/floralset1706/floralset170600120/80446027-billiard-red-pool-ball-with-number-3-snooker-transparent-background-vector-illustration-.jpg"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

token = None

latestEntry=None

userId = None

def GET(url):
    headers = getHeaders()
    return requests.get(url, headers=headers).json()

def POST(url, data):
    headers = getHeaders()
    return requests.post(url, json=data, headers=headers).json()

def getUserId():
    global userId
    if userId is None:
        data={
            'term': user,
            'in_channel_id': mattermostCommandChannel
        }
        response = POST(mattermostApiUrl + "/users/search", data)
        userId = response[0]['id']
        
    return userId

def getHookPayloadBody(message, isAvailable):
    return {
        'channel': 'pool-ping',
        'username': 'pool-ping',
        'text': message,
        'icon_url': availableIconUrl if isAvailable else busyIconUrl
        }

def getHeaders():
    token = getToken()
    return {'Authorization': 'Bearer '+ token }

def updateMattermostAvailable(isAvailable):
    state = "LEDIGT" if isAvailable else "UPPTAGET"
    data = getHookPayloadBody(state, isAvailable)
    POST(mattermostHookUrl, data)
    
def readLatestEntry():
    global mattermostCommandChannel    
    return GET(mattermostApiUrl + '/channels/'+mattermostCommandChannel+'/posts?per_page=1')

def getCommands():
    global latestEntry
    cmds = []
        
    entry = readLatestEntry()
      
    postId = entry['order'][0]
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

def postCurrentConfig(currentConfig):
    msg = "# CURRENT CONFIGURATION\n" + currentConfig
    postToCommandChannel(msg)
    
def postCroppedImage():
    
    poolFinder = PoolTableFinder()
    poolFinder.saveCroppedImage()
    
    postImage(ConfigHandler.getCroppedImagePath())

def postRawImage():
    postImage(ConfigHandler.getCurrentImagePath())

def postImage(path):
    response = uploadImage(path)
    imageId = getImageId(response)

    data = {'channel_id' : mattermostCommandChannel, 'message' : 'Pool table image', 'file_ids': [imageId]}
    POST(mattermostApiUrl + "/posts", data)

def postIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    ip = s.getsockname()[0]

    postToCommandChannel(ip)

def postConfig(key, value):
    msg = str(key) + " : " + str(value)
    postToCommandChannel(msg)

def postScore():
    score = str(ScoreKeeper.score)
    postToCommandChannel(score)

def postToCommandChannel(msg):
    data = {'channel_id' : mattermostCommandChannel, 'message' : msg}
    POST(mattermostApiUrl + "/posts", data)

def postError(msg):
    postToCommandChannel(msg)

def postLog(log):
    postToCommandChannel(log)
    
def getImageId(response):
    return response['file_infos'][0]['id']
    
def uploadImage(path):
    headers = getHeaders()
        
    f = open(path, 'rb')
    formData = {'files': f, 'channel_id' : (None, mattermostCommandChannel)}
    response = requests.post(mattermostApiUrl + "/files", files=formData, headers=headers)
    
    return response.json()

def getPosts(page):
    return GET(mattermostApiUrl + "/channels/" + mattermostCommandChannel + "/posts?page=" + str(page))

def deletePost(post):
    global userId
    headers = getHeaders()
    if post['user_id'] == userId:
        requests.delete(mattermostApiUrl + "/posts/" + str(post['id']), headers=headers).json()

def clearCommandChannelHistory(page):
    getUserId()
    postsResponse = getPosts(page)
    order = postsResponse['order']
    posts = postsResponse['posts']
    
    if len(order) > 0:
        for pId in order:
            p = posts[pId]
            deletePost(p)
        clearCommandChannelHistory(page + 1)
    
def getToken():
    global token
    global user
    global password
    if not token:
        data = {'login_id' : user, 'password': password}
        response = POST(mattermostApiUrl + "/users/login", data)
        token = response.headers['Token']
    
    return token