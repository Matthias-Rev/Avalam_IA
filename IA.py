import cherrypy
import sys
import json
import socket
import threading
import time
import webbrowser
from random import choice
import copy
from random import choice
import math
from tree_search import *


liste_possible=[]
N=0
Path=[]
Moi=None

def Connect_Server():
    global s
    adresse = ("127.0.0.1", 8081)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(adresse)
    print('Correctement connecté')

def send_ping():
    Connect_Server()
    s.connect(('127.0.0.1', 3001))
    with open('ping.json') as file:
        msg=json.loads(file.read())
    ping_msg=json.dumps(msg).encode('utf8')
    totalsend=0
    while totalsend < len(ping_msg):
        print('Message envoyé avec succès !')
        send= s.send(ping_msg[totalsend:])
        totalsend+=send
    time.sleep(2)
    receive()
    
def startBrowser():
    time.sleep(1)
    webbrowser.open('http://127.0.0.1:8080/ping')
    print('Connexion Start !')

def receive():
    finished = False
    msg=''
    while not finished:
        msg += s.recv(4096).decode('utf8')
        try:
            answer = json.loads(msg)
            print(answer)
            finished=True
        except json.JSONDecodeError:
            pass
    s.close()

conserve=Tree('root',[],1,1)

class Server(Tree):
    @cherrypy.expose
    def ping(self):
        send_ping()
        return "pong"
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        global conserve
        global Moi
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        if body !=None:
            board=body['game']
            print(board)
            for x in body['players']:
                if x == body['you']:
                    state=body['players'].index(x)
                    if state == 0:
                        me=True
                    else:
                        me=False
            for _ in range(150):
                board_modified=copy.deepcopy(board)
                conserve._MCTS(board_modified, me)
                board_modified=[]
            choix=conserve._select_best_child()
            del conserve.children[choix[2]+1:len(conserve.children)]
            del conserve.children[0:choix[2]]
            conserve=conserve.children[0]
            move=list(choix[0])
            data={"move": {"from": [int(move[5]), int(move[7])],"to": [int(move[12]), int(move[14])]},"message": "Execute Order 66"}
            return data



if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    startBrowser()

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server(Tree), '', 'IA.conf')