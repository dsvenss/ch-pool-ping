import requests
import json
import asyncio
import websockets
import ssl
import json
from config import ConfigHandler
import time
from datetime import datetime


class MattermostClient:

    def __init__(self):
        self.mattermostConfig = ConfigHandler.getMattermostConfig()

        self.mattermostHookUrl = self.mattermostConfig['webhook']
        self.iconUrl = "http://icons.iconarchive.com/icons/google/noto-emoji-activities/256/52758-pool-8-ball-icon.png"
        self.mattermostApiUrl = self.mattermostConfig['api']
        self.mattermostCommandChannel = self.mattermostConfig['commandChannel']
        self.mattermostStateChannel = self.mattermostConfig['stateChannel']

        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.token = None
        self.user = self.mattermostConfig['user']
        self.password = self.mattermostConfig['password']

        self.latestCommand = None

        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def getPayloadBody(self, message):
        return {
            'channel': 'pool-ping',
            'username': 'pool-ping',
            'text': message,
            'icon_url': self.iconUrl
        }

    def updateMattermostAvailable(self, available):
        state = "LEDIGT" if available is True else "UPPTAGET"
        body = self.getPayloadBody(state)
        response = requests.post(self.mattermostHookUrl, data=json.dumps(body), headers=self.headers)

    def readLatestChannelEntry(self):
        headers = {'Authorization': 'Bearer ' + token}
        return requests.get(self.mattermostApiUrl + '/channels/'+self.mattermostCommandChannel+'/posts?per_page=1',
                            headers=headers).json()

    def parseCommand(self):
        entry = self.readLatestChannelEntry()
        postId = entry['order'][0]
        print('postID ' + str(postId))

        if not self.latestCommand or self.latestCommand['id'] != postId:
            post = entry['posts'][postId]
            cmd = post['message']

        self.latestCommand = entry
        return cmd

    def getMMToken(self):
        global token, user, password
        if not token:
            response = requests.post(self.mattermostApiUrl + "/users/login",
                                     data=json.dumps({'login_id': user, 'password': password}))

        token = response.headers['Token']


getMMToken()
cmd = parseCommand()
print(str(cmd))
