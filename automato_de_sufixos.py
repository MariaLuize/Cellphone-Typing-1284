"""
UNIVERSIDADE FEDERAL DE SANTA CATARINA
DEPARTAMENTO DE INFORMATICA E ESTATISTICA
INE410113-41000025DO/ME (20211) - TEORIA DA COMPUTAÇÃO
TRABALHO I
Alunos: Maria Luize Silva Pinheiro - 202202413
        Rita Carolina Alamino Borges da Costa - 202202412
        William Jones Beckhauser - 202202317
"""
from collections import OrderedDict
from copy import deepcopy

class SANode:
  """
  Classe base para a criação dos nós componentes do Autômato de Sufixo.
  Cada instância desta classe possui como propriedades: length, link, 
  transitions, terminalFlag e rootFlag.
  - length: utilizado para sinalizar o tamanho do maior sufixo aceito por este este estado. 
  - link: usado para identificar o estado externo que possui o mais longo sulfixo presente  
    no estado em análise.
  - transitions: dicionário catalogador de todas as transições que saem do nodo atual.
  - terminalFlag: flag utilizada para indicar se o nodo atual representa um estado 
    de aceitação terminal do Automato de Sufixo.
  - rootFlag: flag identificadora da raiz princial do Automato de Sufixo.
  """
  def __init__(self, length = None, link = None, transitions = None, terminalFlag = False, rootFlag = False):
    self.length       = length
    self.link         = link
    self.transitions  = transitions
    self.terminalFlag = terminalFlag
    self.rootFlag     = rootFlag

class SuffixAutomaton:
  def __init__(self, s=""):
    """
    Classe base para a criação do Autômato de Sufixo.
    Cada instância desta classe possui como propriedades: st, last, currentSize.
    - st: dicionário utilizado para gardar os estados componentes do Automato de Sufixo.
    - last: sinaliza o estado correspondente a toda a string vista no momento.
    - currentSize: tamanho atual do Automato de Sufixo.
    """
    self.st           = OrderedDict({0: SANode(0, -1, OrderedDict(), False, True)})
    self.last         = 0
    self.currentSize  = 1
    self(s)

  def insertString(self, newCharacter):
    """
    Adição de cada caractere, pertenciente à string de entrada, a estrutura de Automato de Sufixo.
    Argumentos:
      self: Automato de Sufixo (AS).
      newCharacter: Adição da nova caractere ao AS.
    Returna: Nada
    """
    cur                 = self.currentSize
    self.st[cur]        = SANode(None, None, OrderedDict(), False, False)
    self.st[cur].length = self.st[self.last].length + 1     
    p = self.last
    while p > -1 and self.st[p].transitions.get(newCharacter) is None:
      self.st[p].transitions[newCharacter] = cur
      p = self.st[p].link  
    if p == -1:
      self.st[cur].link = 0
    else:
      q = self.st[p].transitions.get(newCharacter)
      if self.st[p].length + 1 == self.st[q].length:
        self.st[cur].link = q
      else:
        self.currentSize += 1
        self.st[self.currentSize] = SANode(self.st[p].length + 1, self.st[q].link, deepcopy(self.st[q].transitions))        
        while p > -1 and self.st[p].transitions.get(newCharacter) == q:
          self.st[p].transitions[newCharacter] = self.currentSize
          p = self.st[p].link        
        self.st[q].link = self.st[cur].link = self.currentSize
    self.currentSize += 1
    self.last = cur

  def terminalsDetection(self):
    """
    Identificação dos estados terminais presentes no Automato de Sufixo.
    Esta função mapeia todos os estado do AS, atualizando a sua propriedade terminalFlag.
    Argumentos:
      self: Automato de Sufixo.
    Returna: Nada.
    """
    i = self.last
    while(i > -1):
      if (self.st[i].link == -1): return
      else:
        self.st[i].terminalFlag = True
        i = self.st[i].link
    
  def __call__(self, targetString):
    """
    Chamada das funções insertString e terminalsDetection após a criação do Automato de Sufixo
    Argumentos:
      self: Automato de Sufixo (AS).
      targetString: string utilizada para o preenchimento do AS.
    Returna: Nada.
    """
    for character in targetString:
      self.insertString(character)
    self.terminalsDetection()