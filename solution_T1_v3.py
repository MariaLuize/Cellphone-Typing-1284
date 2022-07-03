"""
UNIVERSIDADE FEDERAL DE SANTA CATARINA
DEPARTAMENTO DE INFORMATICA E ESTATISTICA
INE410113-41000025DO/ME (20211) - TEORIA DA COMPUTAÇÃO
TRABALHO I
Alunos: Maria Luize Silva Pinheiro - 202202413
        Rita Carolina Alamino Borges da Costa - 202202412
        William Jones Beckhauser - 202202317
"""
class TrieNode:
  """
  Classe base para a criação dos nós componentes da árvore.
  Cada nó possui um array de tamanho 26, ao qual é inicialmente preenchido por None's.
  Ainda, cada nó possui um atributo 'flag_leaf', ao qual sinaliza se determinado nó representa o final da palavra inserida.
  __slots__ são estrutura de custominação de acesso aos atributos da Instância. Utilizarlos significa otimizar o acesso aos atributos (https://wiki.python.org/moin/UsingSlots)
  """
  __slots__ = ('children', 'flag_terminal','__dict__')
  def __init__(self):
    self.children  = [None] * 26
    self.flag_leaf = False

def add_string(root_trie, word):
  """
  Inserção de palavra na árvore.
  Esta função se utiliza do nó raiz para a inserção de novas palavras por meio
  da criação de novos nós com seu array de filhos. Tal array representa as letras 
  posteriores a letra a qual o nó diz respeito, de forma que na palavra rei, e é 
  a letra imediatamente seguinte de seu "nó pai", r.
  A posição ocupada por uma letra hipotética, no array de filhos de seu nó pai, 
  é calculada pior meio da diferença entre o valor de tal letra em código unicode,
  e o valor do caracter 'a' também em código unicode.
  Após isso, a letra correntemente analisada é atualizada como a raiz, ou nó pai, da
  próxima letra da palavra. Ao chegar ao finalda palavra, o parâmetro 'flagLeaf' é 
  atualizado para True
  Argumentos:
    root_trie: nó raiz da árvore Trie
    word: palavra a ser inserida na Trie
  Returna: Nada
  """
  root = root_trie
  length = len(word)
  for level in range(length):
    index = ord(word[level])-ord('a')
    if not root.children[index]:root.children[index] = TrieNode()
    root = root.children[index]
  root.flag_leaf = True
def prefix_count(root_trie, word):
  """
  Contagem de decisões necessárias para a busca de uma palavra presente na Trie.
  Tal análise é feita por meio do cálculo de nodos que possuem mais de uma posição válida
  em seus array de filhos e ainda não se chegou ao final da palavra (último nível da 
  árvore em que a palavra em questão esta presente). Estes cenários representam momentos 
  de decisão entre mais de uma alternativa. Ainda, é considerado momentos em que um nó 
  possui apenas uma posição preenchida em seu array de nós filhos, porém tal nó é 
  identificado como um nó folha de alguma palavra, em tal ocasião, 1 é adicionado a 
  contagens de decisões para a referida palavra 
  Argumentos:
    root_trie: nó raiz da árvore Trie
    word: palavra a ser contada a quantidade mínima de dígitos necessários para sua 
          formação pela Trie
  Returna: Quantidade de dígitos necessários
  """
  ans    = 1
  root   = root_trie
  length = len(word)
  for level in range(length):
    index = ord(word[level])-ord('a')
    root = root.children[index]
    sum_children = 0
    for child in root.children:
      if child is not None:sum_children+=1
    if (sum_children > 1 and level != (length-1)) or (sum_children == 1 and root.flag_leaf and level != (length-1)):
      ans+=1
  return ans
while True:
  try:
    numEnts = int(input())  # Detecta o número de entradas N
    dictionary = []         # Inicialização do array por armazenar a lista de palavras a serem declaradas pelo usuário
    rootTrie = TrieNode()       # Criação do nó raiz da Trie
    
    for _ in range(numEnts): # Loop para a detecção das palavras, adição destas ao array dictionary, e subsequente adição à árvore
      word = input()
      dictionary.append(word)
      add_string(rootTrie,word)

    answer = 0 # Variável relativa a somatória das quantidades mínimas de digitos necessários para todas cada palavras do dicionário analisado
    
    for word in dictionary:answer += prefix_count(rootTrie, word) # Loop pela submissão das palavras do dicionário à função prefix_count,
                                                                  # e atualização do valor da variável answer
    print("%.2f" %(answer/numEnts)) # Média de decisões necessárias para digitar uma palavra do dicionário
  except EOFError:
    break