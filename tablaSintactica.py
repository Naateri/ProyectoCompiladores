class TablaSintactica:

    def __init__(self):
        self.tabla = dict()
        self.PADDING = 8
        self.terminales = {'$', 'lambda'}
        self.noterminales = set()
    
    def insertar(self, noterminal, terminal, value):
        if noterminal not in self.tabla:
            # si no existe, crearlo
            self.tabla[noterminal] = dict()
            self.noterminales.add(noterminal)
        # Insertar arreglo en la entrada    
        self.tabla[noterminal][terminal] = value
        self.terminales.add(terminal)
    
    # print(tablaSintactica)
    def __str__(self):
        ret_str = ''
        # Todos los strings tienen len=padding
        # Para que se vea ordenado
        ret_str += " ".ljust(self.PADDING)
        # Imprimir terminales arriba
        terminal_list = list(self.terminales)
        for term in terminal_list:
            ret_str += term.ljust(self.PADDING)

        ret_str += '\n'

        # Recorriendo tabla
        for non_term in list(self.noterminales):
            # Imprimir no terminal a la izquierda
            ret_str += non_term.ljust(self.PADDING)
            for term in terminal_list:
                # Si no hay valor en la casilla
                # Imprimir vacío
                if term not in self.tabla[non_term]:
                    ret_str += " ".ljust(self.PADDING)
                else:
                    # Imprimir produccion si hay valor
                    produccion = ""
                    if type(self.tabla[non_term][term]) == type(None):
                        print("NT", non_term)
                        print("T", term)
                    for value in self.tabla[non_term][term]:
                        produccion += value
                    ret_str += produccion.ljust(self.PADDING)
            ret_str += '\n'
        
        return ret_str
