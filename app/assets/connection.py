#for getting and posting data
import json.decoder
import requests
import sys
from urllib import request,response #its request in python 3 but load in python 2
class Conn(object):
    def __init__(self,site,port):
        self.site=site
        self.port=port
    def get(self,uri):
        self.uri=uri
        _url='http://'+self.site+":"+self.port+self.uri
        r = requests.get(_url)

        return r.json()

    def post (self,uri,data):
        #default headers
        self.data=data
        self.uri=uri
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        _url='http://'+self.site+":"+self.port+self.uri
        #params = urllib.urlencode(post_params)
        p = requests.post(_url,body)
        return p







