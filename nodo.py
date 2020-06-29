### Arbol sintáctico ###

class Nodo:
    etiqueta = ''
    hijos = list() # lista de referencias a los nodos hijos
    padre = None
    siguiente = None # hermano

    def __init__(self, label):
        self.etiqueta = label
