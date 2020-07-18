from analizadorLexico import AnalizadorLexico
from analizadorLexico import Token
from produccion import Produccion
from tablaSintactica import TablaSintactica
from nodo import Nodo
from error_log import Log
from translator import Translator

def opera1(pivote, literales):
    # adicionar cada literal al nodo pivote
    for cur_child in range(len(literales)):
        pivote.hijos.append(Nodo(literales[cur_child]))
    # hermanos
    for cur_child in range(len(literales)-1):
        pivote.hijos[cur_child].siguiente = pivote.hijos[cur_child]
    # retornar referencia al primer hijo (por la izq)
    return pivote.hijos[0]

def opera2(pivote):
    # retornar referencia al siguiente hermano
    if pivote.siguiente is not None:
        return pivote.siguiente
    # si no hay: retornar siguiente del hermano del padre
    if pivote.padre is not None:
    # si no hay continuar hasta encontrar
        return opera2(pivote.padre)
    # un hermano o el nodo raiz
    # en el ultimo caso retornar vacio (None)
    return None

def opera3(pivote):
    # adicionar el operador lambda en el nodo donde se encuentre
    pivote.hijos.append('lambda')
    # retornar opera2(pivote)
    return opera2(pivote)    


class Gramatica:
    # Impresion de la tabla
    PADDING = 15
    producciones = []
    # Ventaja de usar lista:
    # poder meter más de una vez de manera sencilla
    # producción que empieza
    # con el mismo no terminal, ej (uno después del otro):
    # Gramatica.cargar("Ep := A|B")
    # Gramatica.cargar("Ep := C|D")
    terminales = set()
    noterminales = set()
    siguientes = None # siguientes de no terminales
    dolar = '$'
    analizador_lexico = None

    log = Log().get_instance() # Log de errores y warnings
    translator = None

    def __init__(self):
        #terminales = ['+', '-', '*', '/', '(', ')', 'num', 'id', '$']
        #noterminales = ['E', 'Ep', 'T', 'Tp', 'F']
        self.nodoInicial = None
        self.tablaSintactica = None
        self.terminales.add('$') # Fin de cadena
        self.analizador_lexico = AnalizadorLexico()
        self.translator = Translator()

    # getIzquierdaFromDerecha:
    # encontrar generador de la izquierda a partir de toda
    # una oracion a la derecha
    def getIzquierdaFromDerecha(self, right_sent):
        # Buscando en todas las producciones
        for produccion in self.producciones:
            # En las derechas
            for right in produccion.right:
                # Si la derecha coincide
                if right.strip() == right_sent.strip():
                    # Hicimos match
                    return produccion.left.replace(' ', '')

    # getProduccion: lado derecho generado por
    # valor a la izquierda (izq)
    def getProduccion(self, izq):
        # Buscando en el conjunto de producciones
        ret_value = list()
        for produccion in self.producciones:
            # Eliminando espacios en blanco
            # En caso sea necesario
            # Si coincide, retornar produccion
            if produccion.left.replace(' ', '') == izq:
                for right in produccion.right:
                    ret_value.append(right)
                
                # No se rompe el bucle porque puede que
                # Un valor a la izquierda tenga múltiples
                # valores a la derecha
        return ret_value

    # get producciones: todos los elementos de la derecha
    # de la gramatica
    def getProducciones(self):
        # retornar elementos de la derecha en forma de una lista
        producciones = list()
        for nodo in self.noterminales:
            producciones.append(self.getProduccion(nodo))
        return producciones

    # Find generator: generar no terminal que genere el valor
    # indicado en right
    def find_generator(self, right):
        # Encontrar no terminales que generen un valor (right)
        generators = set()
        for produccion in self.producciones:
            # values = arreglo de "derechas"
            values = produccion.right
            # value = string de la produccion
            for value in values:
                if right in value:
                    generators.add(produccion.left)
        # Eliminando a si mismo como su generador en caso se encuentre
        if right in generators:
            generators.remove(right)

        return generators

    def buildTerminals(self):
        # Construye conjunto de terminales
        # Y no terminales segun contenido actual de la
        # Gramatica
        for produccion in self.producciones:
            cur_left = produccion.left.replace(' ','')
            # izquierda siempre es no terminal
            if cur_left not in self.noterminales:
                self.noterminales.add(cur_left)

            # eliminamos en caso este en terminales
            if cur_left in self.terminales:
                self.terminales.remove(cur_left)
            
            for cur_right in produccion.right:
                tokens = cur_right.strip().split(' ')
                for token in tokens:
                    if len(token) < 1:
                        continue
                    # si token esta en no terminales
                    # no se mete a terminales
                    if token not in self.noterminales:
                        self.terminales.add(token)

    # Retornar primeros de un no terminal
    def getPrimero(self, izq):
        primeros = list()

        # Buscamos en las producciones 
        for produccion in self.producciones:
            # Hasta encontrar presencia a la izquierda
            if produccion.left.replace(' ', '') == izq:
                # Buscamos en los resultados a la derecha
                for right in produccion.right:
                    # right.strip(): eliminar espacios en blanco
                    # al inicio y al final
                    tokens = right.strip().split(' ')
                    # si primer nodo/token a la derecha es terminal, es primero
                    if tokens[0] in self.terminales:
                        primeros.append(tokens[0])
                    # si no, getprimero a ese nodo
                    else:
                        nt_primeros = self.getPrimero(tokens[0])
                        primeros = primeros + nt_primeros

        return primeros

    def getPrimeros(self):
        # retorna los primeros de cada nodo
        # no terminal de la gramatica
        primeros = dict()
        for nodo in self.noterminales:
            cur_primeros = self.getPrimero(nodo)
            primeros[nodo] = cur_primeros

        return primeros

    def getSiguientes(self):
        siguientes = dict()

        # Inicializar diccionario
        for noterminal in self.noterminales:
            siguientes[noterminal] = set()
        
        siguientes[self.nodoInicial].add(self.dolar)
        to_fill = list() # valores que no tienen nodo a la derecha
        derechas = list() # valores completos a la derecha de aquellos
        # nodos que no tengan nodo a la derecha (hallar generador correcto)

        for nodo in self.getProducciones():
            # nodo: arreglo con valores a la derecha
            # de un no terminal
            for right_prods in nodo:
                #right_prods: string (un valor a la derecha)
                tokens = right_prods.split()
                for i in range(len(tokens)-1):
                    # Si el token actual es terminal, ignorar
                    if tokens[i] in self.terminales:
                        continue
                    
                    # Si el token siguiente es terminal, es el siguiente (?)
                    # Ej: siguientes de E: {$, (, +, -} (sacado de la practicac)
                    if tokens[i+1] in self.terminales:
                        siguientes[tokens[i]].add(tokens[i+1])
                    else:
                        # El siguiente de un nodo es el primero de su derecha
                        primeros = self.getPrimero(tokens[i+1])
                        for primero in primeros:
                            if primero.strip() != 'lambda':
                                siguientes[tokens[i]].add(primero)
                            # Si un primero es el elemento vacío
                            # El siguiente será el siguiente del lado izquierdo
                            # De su produccion original
                            else:
                                # En nuestro caso, guardamos el no terminal
                                # Para actualizarlo posteriormente con su siguiente
                                siguientes[tokens[i]].add(tokens[i+1])

                    # Si el almacenado es un no terminal, se actualizará
                    # Con el siguiente correspondiente (el de ese no terminal)
                    # después
                        
                # Si el ultimo es no terminal, no tiene
                # nadie a su derecha, lo guardamos en la lista
                # to_fill para actualizarlo posteriormente
                # Regla: su siguiente será el siguiente del lado
                # izquierdo de su produccion original
                if tokens[-1] in self.noterminales:
                    # Solo si no tiene elementos en sus siguientes
                    if len(siguientes[tokens[-1]]) < 1:
                       to_fill.append(tokens[-1])
                       derechas.append(right_prods)

        # Llenando no terminales
        # Que no tenían nodo a su derecha
        for i in range(len(to_fill)):
            # Encontrando quien lo genera
            generated_by = self.getIzquierdaFromDerecha(derechas[i])
            # Reemplazando con los siguientes del generador
            siguientes_generator = siguientes[generated_by]
            for siguiente in siguientes_generator:
                siguientes[to_fill[i]].add(siguiente)

        # Actualizando los que tenían un "siguiente"
        # No terminal con los siguientes de dicho
        # No terminal
        for key in siguientes:
            siguientes_key_copy = list(siguientes[key])
            for siguiente in siguientes_key_copy:
                # si uno de los siguientes es un no terminal
                if siguiente in self.noterminales:
                    # metemos los siguientes de ese no terminal
                    for element in siguientes[siguiente]:
                        if element not in siguientes[key]:
                            siguientes[key].add(element)
                    # eliminamos no terminal de los siguientes
                    siguientes[key].remove(siguiente)

        ## agregar $ a siguientes si tiene vacío como primero

        for noterminal in self.noterminales:
            primeros = self.getPrimero(noterminal)
            if 'lambda' in primeros:
                siguientes[noterminal].add('$')

        self.siguientes = siguientes

        for noterminal in self.noterminales:
            if len(self.siguientes[noterminal]) <= 0:
                self.finish_siguientes(noterminal)

        return siguientes

    def finish_siguientes(self, noterminal):
        # siguiente es vacío, actualizamos
        # con los siguientes del generador
        #print('finish_siguientes')
        #print('noterminal', noterminal)
        gen_by = self.find_generator(noterminal)
        generated_by = list(gen_by)[0]
        # Reemplazando con los siguientes del generador
        siguientes_generator = self.siguientes[generated_by]
        # Generador tiene sus siguientes vacíos
        if len(siguientes_generator) <= 0:
            self.finish_siguientes(generated_by)
        for siguiente in siguientes_generator:
            self.siguientes[noterminal].add(siguiente)

    def buscar_produccion(self, noterminal, terminal):
        producciones = self.getProduccion(noterminal)
        # Si solo se genera una producción
        # Retornar esa producción
        if (len(producciones) <= 1):
            return producciones[0]
        # En las producciones generadas por no terminal
        for produccion in producciones:
            # Retornar la que contenga al terminal
            if produccion.find(terminal) != -1:
                return produccion
        print('nt', noterminal, 't', terminal)
        print(producciones)

    def crearTabla(self):
        self.tablaSintactica = TablaSintactica()

        for nodoNt in self.noterminales:
            for nodoT in self.getPrimero(nodoNt):
                if nodoT != 'lambda':
                    produccion = self.buscar_produccion(nodoNt, nodoT)
                    if type(produccion) == type(None):
                        continue
                    self.tablaSintactica.insertar(nodoNt, nodoT,
                        self.buscar_produccion(nodoNt, nodoT))
                else:
                    for nodoT2 in self.siguientes[nodoNt]:
                       self.tablaSintactica.insertar(nodoNt, nodoT2,
                           'lambda')

    def tokenize_array(self, array):
        ret_str = ''
        for value in array:
            ret_str += (value + ' ')
        
        return ret_str

    # Validar String
    def validate_str(self, cadena, linea=0):
        lexico = self.analizador_lexico

        lexic_tokens = lexico.analizadorLexico(cadena)

        queue = [token.valor_gramatica for token in lexic_tokens]

        print(queue)

        # Buscando errores analizador léxico
        for value in queue:
            if value == 'NoOp': # Error operador invalido
                self.log.addError('E0', linea, cadena)
            elif value == 'NoNum': # Error numero invalido
                self.log.addError('E1', linea, cadena)
            elif value == 'NoId': # Error variable no declarada
                self.log.addError('E4', linea, cadena)

        if (len(self.log.get_instance().errores) > 0 or
            len(self.log.get_instance().warnings) > 0):
            print(self.log.get_instance())
            self.log.get_instance().errores.clear()
            self.log.get_instance().warnings.clear()
            return False
        
        #queue = cadena.split()
        
        #print (self.tokenize_array(queue))
        #print ([prod.right for prod in self.producciones])

        real_values = [str(token.palabra) for token in lexic_tokens]

        queue = lexic_tokens
        stack = list()

        stack.append(self.dolar)
        stack.append(self.nodoInicial)
        queue.append(Token(self.dolar, -1, '$', '$'))

        tabla_arbol = [['pila', 'entrada', 'operacion', 'adicionar']]

        raiz = Nodo(self.nodoInicial)
        pivote = raiz

        while (len(stack) > 0 and len(queue) > 0):
            fila_tabla = list()
            queue_vals = [token.valor_gramatica for token in queue]
            fila_tabla.append(self.tokenize_array(stack))
            fila_tabla.append(self.tokenize_array(queue_vals))
            #print('queue', [q.valor_gramatica for q in queue])
            #print('stack', stack )
            # Si queue.top es igual a stack.top()
            if queue[0].valor_gramatica == stack[-1]:
                # pop a cada estructura
                queue.pop(0)
                stack.pop()
                pivote = opera2(pivote)
                fila_tabla.append('2') # operacion 2
                fila_tabla.append(' ')
            else:
                # pop a stack
                temp = stack.pop()
                #print('stack pop', temp)
                try:
                    # Buscar en la tabla
                    valor_tabla = self.tablaSintactica.tabla[temp][queue[0].valor_gramatica]
                    tokens_vtabla = valor_tabla.split()
                    tokens_vtabla.reverse()

                    adicionar_str = '' # adiciones al stack

                    # Visitar tabla en reversa
                    for x in tokens_vtabla:
                        # si existe cadena vacía, la metemos al stack 
                        if x.strip() != 'lambda':
                            stack.append(x)
                            adicionar_str += (x + ' ')
                    
                    if adicionar_str == '':
                        pivote = opera3(pivote)
                        fila_tabla.append('3') # operacion 3
                        fila_tabla.append('lambda')
                    else:
                        pivote = opera1(pivote, adicionar_str.split())
                        fila_tabla.append('1') # operacion 1
                        
                        # Poniendo el orden de los terminales/noterminales
                        # al revés
                        reverse_adicionar = adicionar_str.split()
                        adicionar_str = ''
                        
                        for valor in reverse_adicionar[::-1]:
                            adicionar_str += (valor + ' ')

                        fila_tabla.append(adicionar_str)

                except KeyError:
                    # Si no se encontró valor en la tabla
                    # Se halló un error de sintaxis
                    print("Error de sintaxis")
                    return False
            tabla_arbol.append(fila_tabla)
        
        for fila in tabla_arbol:
            for columna in fila:
                print(columna.ljust(30), end = ' ')
            print()
        
        if len(stack) == 0 and len(queue) == 0:
            self.translator.write_to_file(real_values)
            print('Written values')

        return len(stack) == 0 and len(queue) == 0

    def cargar(self, texto):
        check_newlines = texto.split('\n')
        # Si es multilinea: separando cada linea
        for word in check_newlines:
            if len(word) <= 1:
                continue
            # Armando produccion
            produccion = Produccion(word)
            # Almacenando produccion
            self.producciones.append(produccion)
            if (len(self.producciones) == 1):
                self.nodoInicial = produccion.left.strip()

        self.buildTerminals()

    # print(Gramatica)
    def __str__(self):
        # String a ser retornado
        return_string = ""
        # Recorriendo producciones
        for produccion in self.producciones:
            return_string += (produccion.left + " := ")
            for i in range(len(produccion.right)):
                # Dando formato al resultado
                # Ultimo elemento: no imprimir |
                if i == len(produccion.right) - 1:
                    return_string += (produccion.right[i])
                # No es ultimo elemento: imprimir |
                else:
                    return_string += (produccion.right[i]) + " | "
            return_string += '\n'

        return return_string

    # Deprecated
    # Usar print(tabla)
    def imprimirTabla(self):

        tabla = self.tablaSintactica.tabla
        # Todos los strings tienen len=padding
        # Para que se vea ordenado
        print(" ".ljust(self.PADDING), end = ' ')
        # Imprimir terminales arriba
        terminal_list = list(self.terminales)
        for term in terminal_list:
            print(term.ljust(self.PADDING), end = ' ')

        print()
        # Recorriendo tabla
        for non_term in list(self.noterminales):
            # Imprimir no terminal a la izquierda
            print(non_term.ljust(self.PADDING), end = ' ')
            for term in terminal_list:
                # Si no hay valor en la casilla
                # Imprimir vacío
                if term not in tabla[non_term]:
                    print(" ".ljust(self.PADDING), end = ' ')
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    for value in tabla[non_term][term]:
                        produccion += value
                    print(produccion.ljust(self.PADDING), end = ' ')
            print()
