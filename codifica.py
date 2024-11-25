from cffi import FFI
import os


__all__ = ["compacta","descompacta"]

# Inicializar o FFI
ffi = FFI()

# Declarar a função C
ffi.cdef("""
    int compacta(const char* nomeArqBin, const char* nomeArqTxt);
int descompacta(const char* nomeArqBin, const char* nomeArqTxt);
""")

try:
    c_lib = ffi.dlopen(os.path.abspath("./codifica.dll"))
except OSError as e:
    print(f"Erro ao carregar biblioteca: {e}")


# Objetivo: Compacta o conteudo do arquivo de nome 'nomeArqIn', e armazena o conteudo comapctado arquivo de nome 'nomeArqOut'
# Acoplamento:
#   - Parâmetros de entrada:
#       - nomeArqIn (string): Nome do arquivo que sera compactado.
#       - nomeArqOut (string): Nome do arquivo onde será escrito o texto compactado
#   - Retorno:
#       - código: int.
# Assertivas de entrada:
#   - 'nomeArqIn' deve ser uma string não vazia.
#   - 'nomeArqIn' conter um nome de um arquivo existente.
#   - 'nomeArqOut' deve ser uma string não vazia.
#   - 'nomeArqIn' deve ser diferente de 'nomeArqOut'
# Assertivas de saída:
#   - O contrudo compactado do arquivo de nome 'nomeArqIn' é escrito no arquivo de nome 'nomeArqOut'
def compacta(nomeArqIn, nomeArqOut):
    if nomeArqIn == "" or nomeArqOut == "":
        return 2
    if nomeArqIn == nomeArqOut:
        return 3
    return c_lib.compacta(ffi.new("char[]", nomeArqIn.encode('ascii')),ffi.new("char[]", nomeArqOut.encode('ascii')))



# Objetivo: Compacta o conteudo do arquivo de nome 'nomeArqIn', e armazena o conteudo comapctado arquivo de nome 'nomeArqOut'
# Acoplamento:
#   - Parâmetros de entrada:
#       - nomeArqIn (string): Nome do arquivo que sera descompactador.
#       - nomeArqOut (string): Nome do arquivo onde será escrito o texto descompactado
#   - Retorno:
#       - código: int.
# Assertivas de entrada:
#   - 'nomeArqIn' deve ser uma string não vazia.
#   - 'nomeArqIn' conter um nome de um arquivo existente.
#   - O conteudo do arquivo de nome 'nomeArqIn' deve ter sido gerado por uma chamada da função compacta
#   - 'nomeArqOut' deve ser uma string não vazia.
#   - 'nomeArqIn' deve ser diferente de 'nomeArqOut'
# Assertivas de saída:
#   - O contrudo descompactadp do arquivo de nome 'nomeArqIn' é escrito no arquivo de nome 'nomeArqOut'
def descompacta(nomeArqIn, nomeArqOut):
    if nomeArqIn == "" or nomeArqOut == "":
        return 2
    if nomeArqIn == nomeArqOut:
        return 3
    return c_lib.descompacta(ffi.new("char[]", nomeArqIn.encode('ascii')),ffi.new("char[]", nomeArqOut.encode('ascii')))
