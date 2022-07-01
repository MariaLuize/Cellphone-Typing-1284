/*
UNIVERSIDADE FEDERAL DE SANTA CATARINA
DEPARTAMENTO DE INFORMATICA E ESTATISTICA
INE410113-41000025DO/ME (20211) - TEORIA DA COMPUTAÇÃO
TRABALHO I
Alunos: Maria Luize Silva Pinheiro - 202202413
        Rita Carolina Alamino Borges da Costa - 202202412
        William Jones Beckhauser - 202202317
*/
#include <bits/stdc++.h>
using namespace std;
  
const int alphabetSize = 26;
struct TrieNode
{
    /*
        Classe base para a criação dos nós componentes da árvore.
        Cada nó possui um array de tamanho 26. Ainda, cada nó possui 
        um atributo 'flagLeaf', ao qual sinaliza se determinado nó representa o final da palavra inserida.
    */
    struct TrieNode *children[alphabetSize];
    bool flagLeaf;
};
struct TrieNode *createNode(void)
{
    /*
        Criação dos nodos e população de seus arrays com valores nulos.
        Ainda, seu atributo 'flagLeaf' é inicializado com valor false
        Argumentos: Nada
        Returna: Nodo criado e inicializado
    */
    struct TrieNode *targetNode =  new TrieNode;
    targetNode->flagLeaf = false;
    for (int letter = 0; letter < alphabetSize; letter++)
        targetNode->children[letter] = NULL;
  
    return targetNode;
}
void insertString(struct TrieNode *rootTrie, string word)
{
    /*
        Inserção de palavra na árvore.
        Esta função se utiliza do nó raiz para a inserção de novas palavras por meio
        da criação de novos nós com seu array de filhos. Tal array representa as letras 
        posteriores a letra a qual o nó diz respeito, de forma que na palavra rei, e é 
        a letra imediatamente seguinte de seu "nó pai", r.
        A posição ocupada por uma letra hipotética, no array de filhos de seu nó pai, 
        é calculada pior meio da diferença entre o valor de tal letra em código unicode,
        e o valor do caracter 'a' também em código unicode.
        Após isso, a letra correntemente analisada é atualizada como a raiz, ou nó pai, da
        próxima letra da palavra. Ao chegar ao finalda palavra, o parâmetro 'flagLeaf' é atualizado para true
        Argumentos:
            rootTrie: nó raiz da árvore Trie
            word: palavra a ser inserida na Trie
        Returna: Nada
    */
    struct TrieNode *currentRoot = rootTrie;
    for (int level = 0; level < word.length(); level++)
    {
        int index = word[level] - 'a';
        if (!currentRoot->children[index])
            currentRoot->children[index] = createNode();
        currentRoot = currentRoot->children[index];
    }
    currentRoot->flagLeaf = true;
}
  
int prefixCount (struct TrieNode *rootTrie, string word)
{
    /*
        Contagem de decisões necessárias para a busca de uma palavra presente na Trie.
        Tal análise é feita por meio do cálculo de nodos que possuem mais de uma posição válida
        em seus array de filhos e ainda não se chegou ao final da palavra (último nível da 
        árvore em que a palavra em questão esta presente). Estes cenários representam momentos 
        de decisão entre mais de uma alternativa. Ainda, é considerado momentos em que um nó 
        possui apenas uma posição preenchida em seu array de nós filhos, porém tal nó é 
        identificado como um nó folha de alguma palavra, em tal ocasião, 1 é adicionado a 
        contagens de decisões para a referida palavra 
        Argumentos:
            rootTrie: nó raiz da árvore Trie
            word: palavra a ser contada a quantidade mínima de dígitos necessários para sua 
                formação pela Trie
        Returna: Quantidade de dígitos necessários
    */
    struct TrieNode *root = rootTrie;
    int  count = 1;
    for (int level = 0; level < word.length(); level++)
    {
        int index = word[level] - 'a';
        if (!root->children[index])
            return false;
        root = root->children[index];
        int sumValidChildren = 0;
        for (int child = 0; child < alphabetSize; child++){
            if(root->children[child] != 0){
                sumValidChildren ++;
            }
        }
        if((sumValidChildren > 1 && level!=word.length()-1) || (sumValidChildren == 1 && root->flagLeaf && level!=word.length()-1)){
            count ++;
        }
    }
    return count;
}
  
int main()
{
    int n; // Detecta o número de entradas N, representante do tamanho do dicionário
    while (cin >> n){
        vector<string> dictionary(n); // Inicialização do array por armazenar a lista de palavras a serem declaradas pelo usuário
        struct TrieNode *rootTrie = createNode(); // Criação do nó raiz da Trie
        for (int i = 0; i < n; i++){ // Loop para a adição das componentes de dictionary à árvore
            cin >> dictionary[i];
            insertString(rootTrie, dictionary[i].c_str());   
        }
        double answer = 0; // Variável relativa a somatória das quantidades mínimas de digitos necessários para todas cada palavras do dicionário analisado
        for (int i = 0; i < n; i++) // Loop pela submissão das palavras do dicionário à função prefixCount,
                                    // e atualização do valor da variável answer
          answer += prefixCount (rootTrie, dictionary[i].c_str());
        printf("%.2lf\n",(answer/(double)n)); // Média de decisões necessárias para digitar uma palavra do dicionário
    }
    return 0;
}