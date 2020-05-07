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
#https://www.google.com/search?client=firefox-b-d&q=send+json+socket+python#kpvalbx=_xDiPXprYO463kwXtyLKAAw26
#ip= 127.0.0.1

liste_possible=[]
N=0
Path=[]
Moi=None
#Inverser le premier coup
def tour(num):
    if num == False:
        return 1
    else:
        return 0

def winner(board, turn, number=0):
    if len(verification(board, turn))==0:
        if number==1:
            return True
        else:
            return winner(board, not turn, number=1)
    else:
        return False

def win(board):
    win_0=0
    win_1=0
    for line in board:
        for elem in line:
            if len(elem)!=0:
                if elem[-1]==1:
                    win_1+=1
                else:
                    win_0+=1
    if win_0 > win_1:
        if Moi == True:
            return 1
        else:
            return -1
    elif win_0 < win_1:
        if Moi == True:
            return -1
        else:
            return 1
    else:
        #Pour l'instant ça reste en juste-milieu
        return 0

def verification (board, turn):
    turns=tour(turn)
    number=0
    cas_possible=[]
    for line in board:
        for elem in line:
            if len(elem)!=0:
                if len(possibility(board, number))>0 and elem[-1]==turns:
                    cas_possible.append(number)
            number+=1
    return cas_possible

def possibility (board, case):
    cases=[]
    z=0
    for line in board:
        for elem in line:
                cases.append(elem)
    calcul=[case-10, case-9, case-8, case+1, case+10, case+9, case+8, case-1]
    possible = []
    while True:
        for w in range(0,8):
            try:
                if calcul[w]//9 < 0 or calcul[w]%9 < 0:
                    possible.append([])
                    continue
                number=len(board[calcul[w]//9][calcul[w]%9])+len(board[case//9][case%9])
                if number <6 and len(board[calcul[w]//9][calcul[w]%9]) !=0:
                    possible.append(cases[calcul[w]])
                else:
                    possible.append([])
            except IndexError:
                possible.append([])
        break
    variable_name=["a","b","c","d","e","f","g","h"]
    mvt_possible=[]
    for x in possible:
        if 0<len(x)<5:
            mvt_possible.append(variable_name[z])
        z+=1
    return mvt_possible

def mvt_string(case, destination):
    possible_letter={'a':[case-10],'b':[case-9],'c':[case-8],'d':[case+1],'e':[case+10],'f':[case+9],'g':[case+8],'h':[case-1]}
    for x in possible_letter:
        if x == destination:
            after=possible_letter[x]
            
            return 'move {},{} to {},{}'.format(case//9,case%9,after[0]//9,after[0]%9)

def full_random(board, turn):
    for x in verification(board, turn):
        for y in possibility(board, x):
            next_value=mvt_string(x, y)
            liste_possible.append(next_value)
    return liste_possible

def make_move(board,ligne, colomn, ligne_dest, colomn_dest):
    copy_case=copy.deepcopy(board[ligne][colomn])
    board[ligne][colomn]=[]
    for x in copy_case:
        if len(board[ligne_dest][colomn_dest])<5:
            board[ligne_dest][colomn_dest].append(x)
        else:
            print('roger we have a problem')
    copy_case=[]
    return board


class Tree:
    def __init__(self, value, children=[],exploration=0, win=0):
        self.__value=value
        self.__exploration=exploration
        self.__win=win
        self.__children=copy.deepcopy(children)

    @property
    def children(self):
        return self.__children
    @property
    def value(self):
        return self.__value
    @property
    def size(self):
        result=1
        for x in self.children:
            result+=x.size
        return result
    
    def add_child(self, tree):
        self.__children.append(tree)
    
    def __getitem__(self, index):
        return self.__children[index]
    
    @property
    def _utc(self):
        global N
        calcul=0
        if self.__exploration==0:
            return math.inf
        if N !=0:
            log_N_vertex=math.log(N)
            calcul= (self.__win/self.__exploration)+2*math.sqrt(log_N_vertex/ self.__exploration)
        return calcul
    
    def __str__(self):
        def _str(tree, level):
            result='[{}], {}, {}, ({})\n'.format(tree.__value, tree.__exploration, tree.__win, tree._utc)
            for child in tree.children:
                result+='{}|--{}'.format('  '*level, _str(child, level+1))
            return result
        return _str(self, 0)
    
    def _search(self, value, win):
        for child in self.children:
            if child.value == value:
                child.__exploration+=1
                child.__win+=win
            if len(child.children)!=0:
                return child._search(value, win)
        return
    
    def _delete(self, value, level=0):
        for child in self.children:
            '''if child.size>1:
                return child._delete(value)'''
            if child.value ==value:
                del self.children[0]
                return
    
    #res = 0 1 0.5
    def _MCTS(self, board, turn):
        global N
        if len(self.children) == 0:#feuille
            if self.__exploration==0:#vierge d'exploration
                result= self._rollout(board, turn) #simulation renvoie un resultat #MAJ les résultats ,self.win += res#Simulation+=1
                self.__exploration+=1
                self.__win+=result
                self.__children
                #print(self)
                return result
            else:
                self._expand(board, not turn)
        Nselect = self._select(board)#Donne le meilleur fils utilise l'equation
        res = Nselect[0]._MCTS(Nselect[1], not turn)
        self.__exploration+=1
        self.__win+=res
        N+=1
        #MAJ du resultat dans le noeud courant (win+=res)
        #Simulation+=1
        return res
    
    def _rollout(self, board, turn):#simulation renvoie un resultat
        global liste_possible
        turns=tour(turn)
        winners=winner(board, turns)
        if winners == True:
            wine=win(board)
            return wine
        new_board=self._simulate(board, self.value)
        if len(verification(board, turn)) ==0:
            return self._rollout(board, not turn)
        new_case=choice(full_random(board, turn))
        next_child=Tree(str(new_case))
        liste_possible=[]
        #Path.append(str(new_case))
        return next_child._rollout(new_board, not turn)
    
    def _expand(self, board, turn):
        #liste des coups et ajouter chaque coup comme un noeud et peut etre l'etat du board
        #Liste des coups possibles
        #Ajouter chaque coup comme noeud
        #l'etat du board qui en découle
        all_case_possibility=verification(board, turn)
        for x in all_case_possibility:
            all_deplacement=possibility(board, x)
            for y in all_deplacement:
                self.add_child(Tree(str(mvt_string(x, y))))
        return
    
    def _select(self, board):#Donne le meilleur fils utilise l'equation
        maximum=0
        for child in self.children:
            maximum=max(maximum, child._utc)
            if maximum == child._utc:
                best_child=child.value
        for child in self.children:
            if child.value == best_child:
                new_board=child._simulate(board, child.value)
                return [child , new_board]
    
    def _simulate(self, board, move):
        move_split=list(move)
        board=make_move(board, int(move_split[5]), int(move_split[7]), int(move_split[12]), int(move_split[14]))
        return board

    def _select_best_child (self, maximum=0):
        for child in self.children:
            if child.__exploration==0:
                pass
            else:
                maximum=max(maximum, child._utc)
                if maximum == child._utc:
                    best_child=child.value
                    level=self.children.index(child)
                    
        return best_child, maximum ,level

def Connect_Server():
    global s
    adresse = ("127.0.0.1", 8081) #Changer le port si tu veux
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(adresse)
    print('Correctement connecté')

def send_ping():
    Connect_Server()
    s.connect(('127.0.0.1', 3001))  #Serveur du prof
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
        print(body)
        if body !=None:
            board=body['game']
            #print(board)
            for x in body['players']:
                if x == body['you']:
                    state=body['players'].index(x)
                    print(state)
                    if state == 0:
                        me=True
                    else:
                        me=False
            for _ in range(100):
                board_modified=copy.deepcopy(board)
                conserve._MCTS(board_modified, me)
                board_modified=[]
                print(conserve)
            choix=conserve._select_best_child()
            print('Le {} avec un ucts de {}'.format(choix[0], choix[1]))
            del conserve.children[choix[2]+1:len(conserve.children)]
            del conserve.children[0:choix[2]]
            conserve=conserve.children[0]
            print(conserve)
            move=list(choix[0])
            print(move)
            data={"move": {"from": [int(move[5]), int(move[7])],"to": [int(move[12]), int(move[14])]},"message": "I'm Smart"}
            return data



if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    startBrowser()

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server(Tree), '', 'IA.conf')