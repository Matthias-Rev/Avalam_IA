import copy
from random import choice
import math
import time

liste_possible=[]
N=0
Path=[]
Moi=None

#permet de savoir quelle pion on est
def tour(num):
    if num == False:
        return 1
    else:
        return 0

#determine si qqun sait encore jouer
def winner(board, turn, number=0):
    if len(verification(board, turn))==0:
        if number==1:
            return True
        else:
            return winner(board, not turn, number=1)
    else:
        return False

#Renvoie si c'est une victoire ou une défaite, une égalité
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
        return 0

#vérifie toute les cases possibles à jouer
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

'''
comment  ça marche:  a   b    c
                     h target d
                     e   f    g
garde ça dans une liste [a, b, c]
réponse représente tout les coups possibles d'une case
'''
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

#renvoie une manière plus facile de lire ce qu'il se passe
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

#modifie le board actuel avec le move choisie
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
    
    #l'équation d'exploration dans la sélection
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
            if child.value ==value:
                del self.children[0]
                return
    
    #la fonction principale
    def _MCTS(self, board, turn):
        global N
        if len(self.children) == 0:# si c'est une feuille ou un fils sans fils
            if self.__exploration==0:#vierge d'exploration
                result= self._rollout(board, turn) #autre nom pour la phase simulation
                self.__exploration+=1
                self.__win+=result
                self.__children
                return result
            else:
                self._expand(board, not turn)
        Nselect = self._select(board)#Donne le meilleur fils utilise l'equation
        res = Nselect[0]._MCTS(Nselect[1], not turn)
        self.__exploration+=1
        self.__win+=res
        N+=1
        #MAJ du resultat dans le noeud courant
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
        return next_child._rollout(new_board, not turn)
    
    def _expand(self, board, turn):
        #Liste des coups possibles
        #Ajoute chaque coup comme noeud
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

    #fonction utiliser à la fin pour renvoyer le fils le plus prometteur
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