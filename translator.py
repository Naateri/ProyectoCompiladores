import os

class Translator:
    file = 'result.cpp'

    def __init__(self):
        pass
    
    def translate_call(self, tokens):
        # CALL D_TYPE id = id F
        text = ''
        text += tokens[1] + ' ' # D_TYPE
        text += tokens[2] + ' ' # D_TYPE id
        text += tokens[3] + ' ' # D_TYPE id =
        text += tokens[4] + '(' # D_TYPE id = id(
        text += tokens[5] + ');' # D_TYPE id = id(F);
        return text

    def translate_lambda(self, tokens):
        # LAMBDA D_TYPE id = D_TYPE id : OPERATION
        text = tokens[1] + ' ' # D_TYPE
        text += tokens[2] + '(' # D_TYPE id(
        text += tokens[4] + ' ' # D_TYPE id(D_TYPE 
        text += tokens[5] + '){\n' # D_TYPE id(D_TYPE id){
        text += 'return ' # D_TYPE id(D_TYPE id){
                          # return
        cur_index = 7
        for i in range(cur_index, len(tokens)): # D_TYPE id(D_TYPE id){
            text += tokens[i] + ' '               # return OPERATION;
        text += ';\n}'                            # }
        
        return text
    
    def translate_declaration(self, tokens):
        # D_TYPE id = OPERATION
        text = tokens[0] + ' ' # D_TYPE
        text += tokens[1] + ' ' # D_TYPE id
        text += tokens[2] + ' ' # D_TYPE id =
        cur_index = 3

        for i in range(cur_index, len(tokens)):
            text += tokens[i] + ' ' # D_TYPE id = OPERATION
        text += ';'
        return text

    def translate_output(self, tokens):
        # print F
        text = 'std::cout << '
        text += tokens[1] + ' ' # std::cout << F
        text += '<< std::endl;' # std::cout << F << std::endl
        return text

    def translate_input(self, tokens):
        # INP D_TYPE id = input
        text = tokens[1] + ' ' # D_TYPE
        text += tokens[2] + ';\n' # D_TYPE id;
        text += 'std::cin >> '
        text += tokens[2] + ';' # D_TYPE id;\n std::cin >> id;
        return text

    def translate_if(self, tokens):
        # if F REL_OP F begin
        text = tokens[0] + '( ' # if(
        text += (tokens[1] + ' ' + tokens[2] + ' ' + tokens[3] + ' )')
        # if( F REL_OP F )
        text += '{' # if( F REL_OP F ){
        return text
    
    def translate_else(self, tokens):
        # else begin
        text = tokens[0] + '{' # else {
        return text
    
    def translate_end(self, tokens):
        return '}'
    
    def translate_main(self, tokens):
        return 'int main(){\n'

    def translate(self, tokens):
        if tokens[0] == 'CALL':
            return self.translate_call(tokens)
        elif tokens[0] == 'LAMBDA':
            return self.translate_lambda(tokens)
        elif tokens[0] == 'int' or tokens[0] == 'float':
            return self.translate_declaration(tokens)
        elif tokens[0] == 'print':
            return self.translate_output(tokens)
        elif tokens[0] == 'INP':
            return self.translate_input(tokens)
        elif tokens[0] == 'if':
            return self.translate_if(tokens)
        elif tokens[0] == 'else':
            return self.translate_else(tokens)
        elif tokens[0] == 'end':
            return self.translate_end(tokens)
        elif tokens[0] == 'MAIN':
            return self.translate_main(tokens)

    def write_to_file(self, tokens):
        if not os.path.isfile(self.file):
            f = open(self.file, 'a')
            f.write('#include <iostream>\n\n')

        f = open(self.file, 'a')
        translation = self.translate(tokens)
        f.write(translation + '\n')
        f.close()

    def write_eof(self):
        f = open(self.file, 'a')
        f.write('return 0;\n}')
        f.close()