from gramatica import Gramatica

def main():

    gramatica = Gramatica()
    #gramatica.cargar("Ep := prueba")
    #DECL := NUMTYPE id = OPERATION
    #EXPR := int id = OPERATION | float id = OPERATION
    #OUT := print ( F )
    gramatica.cargar("""
EXPR := int id = OPERATION | float id = OPERATION
EXPR := print ( F )
OPERATION := T Ep
Ep := + T Ep 
Ep := - T Ep
Ep := lambda
T := F Tp
Tp := * F Tp
Tp := / F Tp
Tp := % F Tp  
Tp := lambda
F := id | value
""")
    print(gramatica)

    print("no terminales", gramatica.noterminales)
    print("terminales", gramatica.terminales, '\n')

    primeros = gramatica.getPrimeros()
    print("primeros")
    print(primeros)
    print()

    siguientes = gramatica.getSiguientes()
    print("siguientes")
    print(siguientes)
    print()

    gramatica.crearTabla()
    #gramatica.imprimirTabla()
    print(gramatica.tablaSintactica)

    #cadenas = ['print ( id )', 'float id = value + id * id', 
    #    'int id = value - value % id', 'print ( float )']
    #for cadena in cadenas:
     #   if gramatica.validate_str(cadena) == True:
      #      print(cadena, "Válida")
      #  else:
       #     print(cadena, "No válida")
    texto = """float prueba = 111@3 + 124a
int prueba2 = 12 + 23%14"""
    #cadenas = ['11@3 + 124a', '12 + 23 % 14']
    cadenas = texto.split('\n')
    linea = 0
    for cadena in cadenas:
        gramatica.validate_str(cadena, linea)
        linea += 1

    gramatica.validate_str('float hola = 2+3', 0)
    

if __name__ == '__main__':
    main()
