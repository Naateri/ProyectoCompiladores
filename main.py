from gramatica import Gramatica

def main():

    gramatica = Gramatica()
    #gramatica2 = Gramatica()
    #gramatica.cargar("Ep := prueba")
    #DECL := NUMTYPE id = OPERATION
    #EXPR := int id = OPERATION | float id = OPERATION
    #OUT := print ( F )
    #EXPR := print ( F )
    gramatica.cargar("""
EXPR := D_TYPE id = OPERATION
EXPR := print ( F )
EXPR := if F REL_OP F begin
EXPR := else begin
EXPR := end
EXPR := LAMBDA D_TYPE id = D_TYPE id : OPERATION
EXPR := CALL D_TYPE id = F F
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

    texto = """LAMBDA int potencia2 = int num : num * num  & Declaración función
CALL int prueba_ = potencia2 4 & Llamada a función
int _prueba2 = 12 + 23%14 & Declaración tipo entero
int prueba3 = _prueba2 + 1 & Declaración usando otra variable
float hola = 2*3/5 & Declaración tipo flotante, multiplicación con división
int prueba1 = 5 & Declaración variable prueba1
if prueba1 <= 3 begin & Ejemplo if
int prueba4 = 3+ prueba1 & Contenido del if
int result = prueba1 + prueba4 & Segunda linea if
end & Fin del if"""
    cadenas = texto.split('\n')
    linea = 1
    valid = True
    for cadena in cadenas:
        validate = gramatica.validate_str(cadena, linea)
        if not validate:
            print('Error de compilación')
            valid = False
            break
        linea += 1

    if valid:
        lexical_analyzer = gramatica.analizador_lexico
        cur_balance = lexical_analyzer.get_balance()
        if not lexical_analyzer.balanced_text(cur_balance):
            gramatica.log.addError('E2', 0, 'Revisar todo')
            print(gramatica.log)


    #gramatica.validate_str('float hola = 2+3 & Declaración tipo flotante, suma', 0)

    #gramatica.validate_str('float prueba = 111@3 + 124a & Declaración tipo flotante con error')
    #gramatica.validate_str('if a <= 3 begin')
    

if __name__ == '__main__':
    main()
