class Token:
    palabra = ""
    indice = -1
    tipo = ""
    valor_gramatica = '' # ej: num, id, +, etc

    def __init__(self, palabra, indice, tipo, vg):
        self.palabra = palabra
        self.indice = indice
        self.tipo = tipo
        self.valor_gramatica = vg
    
    def __str__(self): #print(Token)
        return "Token[{0}]: pos = {1}, tipo = {2}, valor = {3}".format(
            self.palabra, self.indice, self.tipo, self.valor_gramatica)

    def toString(self):
        return str(self)
