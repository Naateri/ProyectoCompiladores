from gramatica import Gramatica
import os
import sys, getopt

def main(argv):

    inputfile = ''
    show_tree = True
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile='])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o 0/1 (0=NOshowtree, 1=showtree)')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o 0/1 (0=NOshowtree, 1=showtree)')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt == '-o':
            if str(arg) == '1':
                show_tree = True
            else:
                show_tree = False


    gramatica = Gramatica(show_tree)
    #gramatica2 = Gramatica()
    #gramatica.cargar("Ep := prueba")
    #DECL := NUMTYPE id = OPERATION
    #EXPR := int id = OPERATION | float id = OPERATION
    #OUT := print ( F )
    #EXPR := print ( F )
    gramatica.cargar("""
EXPR := D_TYPE id = OPERATION
EXPR := print F
EXPR := INP D_TYPE id = input
EXPR := if F REL_OP F begin
EXPR := else begin
EXPR := end
EXPR := LAMBDA D_TYPE id = D_TYPE id : OPERATION
EXPR := CALL D_TYPE id = id F
EXPR := MAIN
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
    '''print(gramatica)
    
    print("no terminales", gramatica.noterminales)
    print("terminales", gramatica.terminales, '\n')'''

    primeros = gramatica.getPrimeros()
    #print("primeros")
    #print(primeros)
    #print()

    siguientes = gramatica.getSiguientes()
    #print("siguientes")
    #print(siguientes)
    #print()

    gramatica.crearTabla()
    #gramatica.imprimirTabla()
    #print(gramatica.tablaSintactica)'''

    f = open(inputfile, 'r')

    #cadenas = texto.split('\n')
    cadenas = []
    for x in f:
        if len(x) >= 2:
            cadenas.append(x)
    linea = 1
    valid = True
    for cadena in cadenas:
        linea += 1
        validate = gramatica.validate_str(cadena.replace('\t', '').strip('\n'), linea)
        if not validate:
            print('Error de compilación')
            valid = False
            break
        

    if valid:
        lexical_analyzer = gramatica.analizador_lexico
        cur_balance = lexical_analyzer.get_balance()
        if not lexical_analyzer.balanced_text(cur_balance):
            gramatica.log.addError('E2', 0, 'Revisar todo')
            print(gramatica.log)
        else:
            gramatica.translator.write_eof()

            print('Program execution')
            os.system('g++ result.cpp -o results')
            os.system('./results')

    print('Deleting files')
    try:
        os.remove('result.cpp')
        os.remove('results')
    except:
        pass


    #gramatica.validate_str('float hola = 2+3 & Declaración tipo flotante, suma', 0)

    #gramatica.validate_str('float prueba = 111@3 + 124a & Declaración tipo flotante con error')
    #gramatica.validate_str('if a <= 3 begin')
    

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('main.py -i <inputfile> -o 0/1 (0=NOshowtree, 1=showtree)')
        sys.exit()        
    main(sys.argv[1:])
