#include "codifica.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct elemento Elemento;
struct elemento {
    char data;
    int freq;
    Elemento* esq, * dir;
};

struct compactadora {
    char simbolo;
    unsigned int codigo;
    int tamanho;
};

typedef struct listaCompac
{
    struct compactadora atual;
    struct listaCompac* next;
} ListaCompac;

typedef struct tabelaCompac
{
    int tam;
    ListaCompac* inicio;
    ListaCompac* final;
} TabelaCompac;

typedef struct contadora {
    char simbolo;
    int freq;
} Contadora;

typedef struct tabelaCont {
    int qnt;
    Contadora caracs[256];
} TabelaCont;

typedef union buffer {
    unsigned int fullBuffer;
    unsigned char partBuffer[4];
} Buffer;

static void insereInicio(TabelaCompac*  tabela, char simbolo, unsigned int codigo, int tamanho)
{
    ListaCompac* el = (ListaCompac*)malloc(sizeof(ListaCompac));
    if (el == NULL) {
        printf("Erro ao alocar memória.\n");
        return;
    }
    if (tabela->inicio == NULL)
    {
        tabela->final = el;
    }
    el->atual.codigo =codigo;
    el->atual.simbolo = simbolo;
    el->atual.tamanho = tamanho;
    el->next = tabela->inicio;
    tabela->inicio = el;
    //printf("%d, %c, %d\n",el->atual.codigo,el->atual.simbolo, el->atual.tamanho);
}

static void insereFinal(TabelaCompac*  tabela, char simbolo, unsigned int codigo, int tamanho)
{
    printf("Fim ");
    
    ListaCompac* el = (ListaCompac*)malloc(sizeof(ListaCompac));
    if (el == NULL) {
        printf("Erro ao alocar memória.\n");
        return;
    }
    if (tabela->inicio == NULL)
    {
        tabela->inicio = el;
    }
    el->atual.codigo =codigo;
    el->atual.simbolo = simbolo;
    el->atual.tamanho = tamanho;
    el->next = NULL;
    tabela->final = el;
}

static void escreveTabela(TabelaCompac* tabela, FILE* arqBin) {
    ListaCompac* atual = tabela->inicio;
    fwrite(&tabela->tam, sizeof(int), 1, arqBin);
    while (atual != NULL) {
        fwrite(&atual->atual, sizeof(struct compactadora), 1, arqBin);  // Escreve o dado no arquivo
        atual = atual->next;  // Avança para o próximo nó
        //printf("A");
    }
    fwrite(&tabela->final->atual, sizeof(struct compactadora), 1, arqBin);
}

static void leTabela(TabelaCompac* tabela, FILE* arqBin) {
    int tam;
    fread(&tam,sizeof(int),1, arqBin);
    for (int i = 0; i < tam; i++)
    {
        struct compactadora carac;
        fread(&carac ,sizeof(struct compactadora), 1, arqBin);
        printf("A %d, %c, %d\n",carac.codigo,carac.simbolo, carac.tamanho);
        insereInicio(tabela, carac.simbolo,carac.codigo, carac.tamanho);
    }
}

static void descer(Contadora vet[], int i, int tam) // funcao para descer na heap
{
    int j;
    Contadora aux;
    j = (2 * i) ;
    if (j <= tam) {
        if (j < tam)
            if (vet[j + 1].freq > vet[j].freq)
                j++;
        if (vet[i].freq < vet[j].freq) {
            aux = vet[i];
            vet[i] = vet[j];
            vet[j] = aux;
            descer(vet, j, tam);
        }
    }
}

static void construir1(Contadora vet[], int n) // funcao para construir heap
{
    for (int i = (n / 2) - 2; i >= 0; i--)
        descer(vet, i, n);
}

static void inverterArray(Contadora arr[], int tamanho) // inverte um array
{
    int inicio = 0;
    int fim = tamanho - 1;
    Contadora temp;
    while (inicio < fim) {
        temp = arr[inicio];
        arr[inicio] = arr[fim];
        arr[fim] = temp;
        inicio++;
        fim--;
    }
}

static void insereContadora(TabelaCont* tabela, char carac) // insere elemento na tabela contadora
{
    int qnt = tabela->qnt;
    for (int i = 0; i < qnt; i++) {
        if (tabela->caracs[i].simbolo == carac) {
            tabela->caracs[i].freq += 1;
            //printf("simbolo=%c, freq=%d\n", tabela->caracs[i].simbolo, tabela->caracs[i].freq);
            return;
        }
    }
    tabela->caracs[qnt].simbolo = carac;
    tabela->caracs[qnt].freq = 1;
    tabela->qnt += 1;
    //printf("simbolo=%c, freq=%d\n", tabela->caracs[qnt].simbolo, tabela->caracs[qnt].freq);
    return;
}

static void ordenaContadora(TabelaCont* tabela) // ordena a tabela contadora
{
    int tam = tabela->qnt;
    Contadora* vet = tabela->caracs;
    int m;
    Contadora aux;
    m = tam - 1;
    construir1(vet, tam);
    while (m >= 0) {
        aux = vet[0];
        vet[0] = vet[m];
        vet[m] = aux;
        m--;
        descer(vet, 0, m);
    }
    inverterArray(vet, tam);

}

static Elemento* criaArvoreAux(Elemento** arrayEls, int tam) // constroi a arvore a partir de um array de nos
{
    int fim = tam - 1;
    while (fim > 0) {
        Elemento* novo = (Elemento*)malloc(sizeof(Elemento));
        novo->dir = arrayEls[fim];
        novo->esq = arrayEls[fim - 1];
        novo->freq = novo->dir->freq + novo->esq->freq;
        novo->data = 0;
        arrayEls[fim] = NULL;
        arrayEls[fim - 1] = novo;
        fim--;
        int pos = fim;
        while (pos > 0 && arrayEls[pos]->freq > arrayEls[pos - 1]->freq) {
            Elemento* aux = arrayEls[pos - 1];
            arrayEls[pos - 1] = arrayEls[pos];
            arrayEls[pos] = aux;
            pos--;
        }
    }
    Elemento* raiz = arrayEls[0];
    free(arrayEls);
    return raiz;
}
/*
static void exibe_simetrica(Elemento* p)// exibe a arvore em ordem simetrica
{
    if (p == NULL)
        printf("arvore nao foi criada\n");
    if (p->esq != NULL)
        exibe_simetrica(p->esq);
    printf("ptr_no=%p, carac=%c freq=%d esq=%p dir=%p\n", p, p->data, p->freq,
        p->esq, p->dir);
    if (p->dir != NULL)
        exibe_simetrica(p->dir);
}*/

static TabelaCont* criaTabelaFreq(FILE* arq) // cria a tabela de frequencias
{
    TabelaCont* tabela = (TabelaCont*)malloc(sizeof(TabelaCont));
    tabela->qnt = 0;
    char character;
    while ((character = fgetc(arq)) != EOF) {
        insereContadora(tabela, character);
    }
    insereContadora(tabela, '!');
    ordenaContadora(tabela);
    
    for (int i = 0; i < tabela->qnt; i++) {
        printf("simbolo=%c, freq=%d\n", tabela->caracs[i].simbolo, tabela->caracs[i].freq);
    }

    return tabela;
}

static Elemento* criaArvore(FILE* arq) // cria arvore a partir da tabela de frequencias
{
    TabelaCont* tabela = criaTabelaFreq(arq);
    
    Elemento** montaArvore =
        (Elemento**)malloc(tabela->qnt * sizeof(Elemento*));
    for (int i = 0; i < tabela->qnt; i++) {
        Elemento* el = (Elemento*)malloc(sizeof(Elemento));
        el->data = tabela->caracs[i].simbolo;
        el->freq = tabela->caracs[i].freq;
        el->esq = NULL;
        el->dir = NULL;
        montaArvore[i] = el;
    }
    Elemento* raiz = criaArvoreAux(montaArvore, tabela->qnt);
    //exibe_simetrica(raiz);
    free(tabela);
    return raiz;
}

static char* intParaBinario(unsigned int num) // converte um int para uma string no formato de um binario 
{
    if (num == 0) {
        char* binario = (char*)malloc(2 * sizeof(char));
        strcpy(binario, "0");
        return binario;
    }

    int tamanho = 0;
    unsigned int temp = num;
    while (temp > 0) {
        temp /= 2;
        tamanho++;
    }

    char* binario = (char*)malloc((tamanho + 1) * sizeof(char));
    binario[tamanho] = '\0';

    for (int i = tamanho - 1; i >= 0; i--) {
        binario[i] = (num % 2) + '0';
        num /= 2;
    }

    return binario;
}

static void criaTabelaCompac(Elemento* raiz, TabelaCompac* tabela,
    unsigned int codigo, int tamanho)//  insere um os caracteres na tabela
{
    if (raiz->esq == NULL && raiz->dir == NULL) {
        if (raiz->data == '!') {
            insereFinal(tabela, raiz->data, codigo, tamanho);
        }
        else {
            insereInicio(tabela, raiz->data, codigo, tamanho);
        }
    tabela->tam++;
    printf("simbolo = '%c',codigo = %d, tamanho = %d\n", raiz->data, codigo, tamanho);
    }
    else {
        if (raiz->esq != NULL) {
            criaTabelaCompac(raiz->esq, tabela, (codigo << 1) | 1,tamanho + 1);
        }
        if (raiz->dir != NULL) {
            criaTabelaCompac(raiz->dir, tabela, (codigo << 1), tamanho + 1);
        }
    }
    return;
}

static TabelaCompac* criaTabela(Elemento* raiz)// cria a tabela de compactação 
{
    TabelaCompac* tabela =
        (TabelaCompac*)malloc(sizeof(TabelaCompac));
    tabela->inicio = NULL;
    tabela->final = NULL;
    tabela->tam = 0;
    criaTabelaCompac(raiz, tabela, 0, 0);
    ListaCompac* atual = tabela->inicio;
    
    while(atual != NULL)
    {
        struct compactadora a = atual->atual;
        char* binario = intParaBinario(a.codigo);
        printf("carac=%c, tamanho=%d, codigo=%s\n", a.simbolo,
                a.tamanho, binario);
        free(binario);
        atual = atual->next;
    }
    return tabela;
}

static struct compactadora* buscaTabela(ListaCompac* atual,
    char carac) // busca um caracter na tabela
{
    while(atual != NULL)
    {
        if (atual->atual.simbolo == carac) {
            return &atual->atual;
        }
        atual = atual->next;
    }
    printf("ERRO caracter %c nao esta na tabela", carac);
    return NULL;
}

static void compactaAux(
    FILE* arqTexto, FILE* arqBin,
    TabelaCompac* v) // compacta o arqTexto baseando-se na tabela v e armazena o conteudo compactado em arqBin
{
    Buffer buffer;
    buffer.fullBuffer = 0;
    int lenBuffer = 0;
    unsigned int tempBuffer;
    char character;
    while ((character = fgetc(arqTexto)) != EOF) {
        struct compactadora* carac = buscaTabela(v->inicio, character); // busca a posicao do carac na tabela
        tempBuffer = carac->codigo; // armazena o codigo em um buffer temporario
        tempBuffer = tempBuffer
            << (32 - carac->tamanho -
                lenBuffer); // move o buffer para coloca-lo onde esta a
        // proxima parte vazia no buffer
        buffer.fullBuffer =
            buffer.fullBuffer |
            tempBuffer; // move o conteudo do buffer temporario para o buffer real
        lenBuffer += carac->tamanho;
        while (lenBuffer >= 8) // tem mais de 1 byte no buffer
        {
            fputc(buffer.partBuffer[3], arqBin);        // escreve no arq binario
            buffer.fullBuffer = buffer.fullBuffer << 8; // corrige o buffer
            lenBuffer -= 8;
        }
    }

    tempBuffer = v->final->atual.codigo; // insere o codigo correspondente ao EOT
    tempBuffer = tempBuffer << (32 - v->final->atual.tamanho - lenBuffer);
    buffer.fullBuffer = buffer.fullBuffer | tempBuffer;
    lenBuffer += v->final->atual.tamanho;
    while (lenBuffer >= 8) {
        fputc(buffer.partBuffer[3], arqBin);
        buffer.fullBuffer = buffer.fullBuffer << 8;
        lenBuffer -= 8;
    }
    fputc(buffer.partBuffer[3],
        arqBin); // insere o conteudo restante do buffer no arquivo
    return;
}

static Elemento* criaNo() // cria no
{
    Elemento* novo = (Elemento*)malloc(sizeof(Elemento));
    novo->dir = NULL;
    novo->esq = NULL;
    novo->freq = 0;
    novo->data = 0;
    return novo;
}

static Elemento* criaArvore2(
    TabelaCompac *tabela) // cria a arvore a partir dos valores da tabela compactadora
{
    Elemento* raiz = criaNo();
    Elemento* atual = raiz;
    ListaCompac* v = tabela->inicio;
    unsigned int aux;
    while(v != NULL) // para cada elemento da tabela
    {
        int tamanho = v->atual.tamanho;
        if (tamanho) {

            aux = v->atual.codigo;
            for (int j = 0; j < tamanho; j++) {
                if (((aux >> (tamanho - 1 - j)) & 1)) {
                    if (atual->esq == NULL) // se nao existe filho a direira
                    {
                        atual->esq = criaNo();
                    }
                    atual = atual->esq;
                }
                else {
                    if (atual->dir == NULL) // se nao existe filho a esquerda
                    {
                        atual->dir = criaNo();
                    }
                    atual = atual->dir;
                }
            }
            // se for uma folha
            if ((tamanho != 0)) {
                atual->data = v->atual.simbolo; // guarda o simbolo
                atual = raiz;               // volta pra raiz
            }
        }
        v = v->next;
    }
    return raiz;
}

static void excluiArvore(Elemento* raiz) // libera a memoria ocupada pela arvore
{
    if (raiz == NULL) {
        return;
    }
    excluiArvore(raiz->esq);
    excluiArvore(raiz->dir);
    free(raiz);
}

static void descompactaAux(
    FILE* arqBin, FILE* arqTexto,
    TabelaCompac* tabela) // descompacta o arqBin baseando-se na tabela v e  armazena o conteudo descompactado em arqTexto
{
    Elemento* arvore = criaArvore2(tabela);
    Elemento* noAtual = arvore;
    char character;
    while (fread(&character, sizeof(char), 1, arqBin)) {
        
        //character = fgetc(arqBin);
        for (int i = 0; i < 8; i++) {
            
            if (character >> (7 - i) & 1) // se o ultimo bit for 1
            {
                noAtual = noAtual->esq;
            }
            else {
                noAtual = noAtual->dir;
            }
            if (noAtual->dir == NULL && noAtual->esq == NULL) // se for uma folha
            {
                if (noAtual->data == '!') // se o conteudo dessa folhar for o
                    // caracter correspondente a EOT
                {
                    excluiArvore(arvore);
                    return;
                }
                printf("%c\n",fputc(noAtual->data, arqTexto));
                
                noAtual = arvore; // volta pra raiz
            }
        }
    }
    return;
}

static void compactaArq(FILE* arqTxt, FILE* arqBin)// cria a arvore a partir do arquivo, gera uma tabela a partir dela, chama a funcao compactaAux
{
    Elemento* raiz = criaArvore(arqTxt);
    
    TabelaCompac* tabela = criaTabela(raiz);
    ListaCompac* v = tabela->inicio;
     while(v != NULL)
     {
        //printf("simbolo = '%c',codigo = %d, tamanho = %d\n", v->atual.simbolo, v->atual.codigo, v->atual.tamanho);
        v=v->next;
     }
    free(raiz);
    fseek(arqTxt, 0, SEEK_SET);
    escreveTabela(tabela, arqBin);
    compactaAux(arqTxt, arqBin, tabela);
    free(tabela);
    return;
}

static void descompactaArq(FILE* arqBin, FILE* arqTxt)// le a tabela do arquivo e chama a funcao descompactaAux
{
    TabelaCompac* tabela = (TabelaCompac*)malloc(sizeof(TabelaCompac));
    tabela->tam = 0;
    tabela->inicio = NULL;
    tabela->final = NULL;

    leTabela(tabela, arqBin);
    
    descompactaAux(arqBin, arqTxt, tabela);
    return;
}

int compacta(const char* nomeArqTxt, const char* nomeArqBin)
{
    FILE* arqTxt = fopen(nomeArqTxt, "r");
    if (arqTxt == NULL) {
        printf("Erro ao abrir o arquivo!\n");
        return 1;
    }
    FILE* arqBin = fopen(nomeArqBin, "wb");
    if (arqBin == NULL) {
        printf("Erro ao abrir o arquivo!\n");
        return 1;
    }

    compactaArq(arqTxt, arqBin);

    fclose(arqBin);
    fclose(arqTxt);
    return 0;
}

int descompacta(const char* nomeArqBin, const char* nomeArqTxt)
{
    FILE* arqBin = fopen(nomeArqBin, "rb");
    if (arqBin == NULL) {
        printf("Erro ao abrir o arquivo\n");
        return 1;
    }
    FILE* arqTxt = fopen(nomeArqTxt, "w");
    if (arqTxt == NULL) {
        printf("Erro ao abrir o arquivo!\n");
        return 1;
    }

    descompactaArq(arqBin, arqTxt);

    fclose(arqBin);
    fclose(arqTxt);
    return 0;
}