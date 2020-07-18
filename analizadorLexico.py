#from token import Token

from error_log import Log

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

class Symbol:
    tipo = None
    value = None
    name = None

    def __init__(self, tipo, value, name):
        self.tipo = tipo
        self.value = value
        self.name = name

    def __str__(self):
        ret_str = 'Symbol, name = ' + self.name
        return ret_str

class SymbolTable:
    symbols = []

    def __init__(self):
        pass

    def add_symbol(self, symbol):
        self.symbols.append(symbol)
    
    def check_by_name(self, symbol_name):
        for symbol in self.symbols:
            if symbol.name == symbol_name:
                return True
        return False

    def __str__(self):
        ret_str = ''
        for symbol in self.symbols:
            ret_str += str(symbol) + '\n'
        return ret_str


class AnalizadorLexico:
    operators = ['+','-','*','/', '%', '=']
    datatypes = ['float', 'int']
    reserved_if = ['if', 'else']
    reserved_delim = ['begin', 'end']
    relational_operators = ['==', '!=', '<=', '>=', '<', '>']
    input_output = ['print', 'input']
    token_comentario = '&'
    lambda_func = 'LAMBDA'
    call_func = 'CALL'
    inp_func = 'INP'
    start_main = 'MAIN'
    symbol_table = None
    balance_beginend = ''

    def __init__(self):
        self.symbol_table = SymbolTable()
    
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
            if token == 'begin':
                self.balance_beginend += 'b'
            else:
                self.balance_beginend += 'e'
        elif token in self.input_output:
            token_obj = Token(token, start_idx, 'IO', token) # IO => I/O
        elif token == self.lambda_func:
            token_obj = Token(token, start_idx, 'LAMBDA', token)
        elif token == self.call_func:
            token_obj = Token(token, start_idx, 'CALL', token)
        elif token == self.inp_func:
            token_obj = Token(token, start_idx, 'INP', token)
        elif token == self.start_main:
            token_obj = Token(token, start_idx, 'M', token)
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

                # Tabla de simbolos
                if tokens[-2].palabra == '=':
                    cur_sym = Symbol(token.tipo, token.palabra, tokens[-3].palabra)
                    if not self.symbol_table.check_by_name(tokens[-3].palabra): # No existe
                        self.symbol_table.add_symbol(cur_sym)

            elif linea[index].isalpha() or linea[index] == '_': #Es una palabra
                token,index = self.reconoceVariable(linea, index)

                # Si es una variable no declarada, reportarlo

                tokens_symbol = [token.valor_gramatica for token in tokens]
                tokens_palabra = [token.palabra for token in tokens]

                if (token.valor_gramatica not in self.datatypes and 
                    token.valor_gramatica not in self.reserved_if and 
                    token.valor_gramatica not in self.reserved_delim
                    and token.valor_gramatica not in self.input_output
                    and token.valor_gramatica != self.lambda_func
                    and token.valor_gramatica != self.call_func
                    and token.valor_gramatica != self.inp_func
                    and token.valor_gramatica != self.start_main):
                    if 'LAMBDA' in tokens_symbol: # Funcion lambda
                        #print('lambda', tokens_symbol)
                        #print(tokens_palabra)
                        if '=' not in tokens_symbol:
                            cur_sym = Symbol('F', 0, token.palabra) # Simbolo de la funcion
                            if not self.symbol_table.check_by_name(token.palabra): # No existe
                                self.symbol_table.add_symbol(cur_sym) # Meter funcion
                        else:
                            if ':' in tokens_symbol: # usando id que o está en la tabla de simbolos
                                # O es el parámetro
                                if (token.palabra not in tokens_palabra # no es el parámetro
                                    and not self.symbol_table.check_by_name(cur_sym)): # no fue definida antes
                                    token.valor_gramatica = 'NoId'

                        
                    elif '=' in tokens_symbol or 'if' in tokens_symbol:
                        # Buscar si ya fue declarada
                        print(self.symbol_table)
                        if not self.symbol_table.check_by_name(token.palabra):
                            # No fue declarada pero esta siendo usada, reportarlo
                            token.valor_gramatica = 'NoId'

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

            elif linea[index] == ':': # Dos puntos de funcion lambda
                token = linea[index]
                token_obj = Token(token, index, ':', ':')
                tokens.append(token_obj)
                index += 1
            
            elif linea[index] == self.token_comentario:
                index += 1
                token,index = self.reconoceComentario(linea, index)
                index += 1

            else: # Posible operador
                token,idx = self.reconocePosibleOperacion(linea, index)
                tokens.append(token) #Guardar token
                index += 1

        return tokens

    def get_balance(self):
        return self.balance_beginend

    def balanced_text(self, text):
        stack = list()
        text = text.replace(' ', '')

        opening_brackets = ['b']
        closing_brackets = ['e']

        for character in text:
            if character in opening_brackets:
                stack.append(character)
            else: #character in closing_brackets
                if len(stack) <= 0:
                    return False
                opening_bracket = stack.pop()
                position = opening_brackets.index(opening_bracket)
                if character != closing_brackets[position]:
                    #print("NO")
                    return False

        if len(stack) > 0:
            #print("NO")
            return False
        else:
            #print("SI")
            return True

