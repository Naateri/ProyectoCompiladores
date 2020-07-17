#from token import Token

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

class AnalizadorLexico:
    operators = ['+','-','*','/', '%', '=']
    datatypes = ['float', 'int']
    reserved_if = ['if', 'else']
    reserved_delim = ['begin', 'end']
    relational_operators = ['==', '!=', '<=', '>=', '<', '>']
    token_comentario = '&'

    def __init__(self):
        pass
    
    def reconoceNumero(self, linea, idx):
        start_idx = idx #Para constructor de Token
        token = ""
        while idx < len(linea) and linea[idx].isdigit(): #mientras sea digito
            token += linea[idx] #Agregar al token
            idx += 1

        token_obj = Token(int(token), start_idx, "E", 'value') #Creacion del token
        return token_obj,idx

    def reconocePosibleNumero(self, linea, idx):
        start_idx = idx #Para constructor de Token
        token = ""
        while idx < len(linea) and linea[idx].isdigit(): #mientras sea digito
            token += linea[idx] #Agregar al token
            idx += 1

        num = True

        while idx < len(linea) and linea[idx].isalpha(): # no es espacio
            token += linea[idx]
            idx += 1
            num = False

        if num: # Es numero
            token_obj = Token(int(token), start_idx, "E", 'value') #Creacion del token 
        else:
            token_obj = Token(token, start_idx, 'Er', 'NoNum') # NoNum = error léxico
        return token_obj,idx

    def reconocePosibleOperacion(self, linea, idx):
        token = linea[idx] 
        token_obj = Token(token, idx, "Er", 'NoOp') #Creacion del token
        idx += 1

        return token_obj, idx

    def reconoceVariable(self, linea, idx):
        start_idx = idx #Para constructor de token
        token = ""
        while idx < len(linea) and linea[idx] not in self.operators and linea[idx] != " ":
            #mientras no sea un operador ni un espacio
            token += linea[idx] #Agregar al token
            idx += 1

        if token in self.datatypes: # datatype
            token_obj = Token(token, start_idx, 'D', 'D_TYPE')
        elif token in self.reserved_if:
            token_obj = Token(token, start_idx, 'I', token)
        elif token in self.reserved_delim:
            token_obj = Token(token, start_idx, 'S', token) # S = Scope
        else:
            token_obj = Token(token, start_idx, "V", 'id') #Creacion del token
        return token_obj,idx
    
    def reconoceComentario(self, linea, idx):
        #start_idx = idx
        token = ''
        while idx < len(linea):
            token += linea[idx]
            idx += 1
        print('Comentario:', token)
        return token, idx


    def analizadorLexico(self, linea):
        tokens = list()
        index = 0
        while index < len(linea): #Recorriendo string

            if linea[index].isdigit(): #Es un numero
                #token,index = self.reconoceNumero(linea, index)
                token,index = self.reconocePosibleNumero(linea, index)
                tokens.append(token) #Guardar token

            elif linea[index].isalpha() or linea[index] == '_': #Es una palabra
                token,index = self.reconoceVariable(linea, index)
                tokens.append(token) #Guardar token

            elif linea[index] in self.operators: #Operadores
                token = linea[index] 
                token_obj = Token(token, index, "O",
                        linea[index]) #Creacion del token
                tokens.append(token_obj) #Guardar token
                index += 1

            elif index+2 <= len(linea) and linea[index:index+2] in self.relational_operators:
                # Operador relacional (==, !=, <=, >=)
                token = linea[index]
                token_obj = Token(token, index, 'OR', 'REL_OP')
                tokens.append(token_obj)
                index += 2

            elif linea[index] in self.relational_operators: # Operador relacional (<, >)
                token = linea[index]
                token_obj = Token(token, index, 'OR', 'REL_OP')
                tokens.append(token_obj)
                index += 1

            elif linea[index] == " ": #Espacio
                index += 1 #Omitir
            
            elif linea[index] == self.token_comentario:
                index += 1
                token,index = self.reconoceComentario(linea, index)
                index += 1

            else: # Posible operador
                token,idx = self.reconocePosibleOperacion(linea, index)
                tokens.append(token) #Guardar token
                index += 1

        return tokens
