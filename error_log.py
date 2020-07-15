class DiccionarioError:
    codigos = dict()

    def __init__(self):
        self.codigos = {'E0': 'InvalidOperator', 'E1': 'IncorrectNumber'}

class Log:
    errores = list()
    warnings = list()

    dicError = DiccionarioError()
    dict_error = dicError.codigos

    # Singleton
    __instance__ = None

    def __init__(self):
        if Log.__instance__ is None:
            Log.__instance__ = self
        else:
            raise Exception('Only one Log is allowed.')

    @staticmethod
    def get_instance():
        if not Log.__instance__:
            Log()
        return Log.__instance__

    # Adicionar error
    def addError(self, codigo, errorParametro):
        error_text = str(codigo) + " " + self.dict_error[codigo]
        self.errores.append( (error_text, errorParametro) )

    # Adicionar warning
    def addWarning(self, codigo, warningParametro):
        warning_text = str(codigo) + " " + self.dict_error[codigo]
        self.errores.append( (warning_text, warningParametro) )

    def __str__(self): # Print lista
        lista_errores = ''
        for i in range(len(self.errores)):
            (cur_error, linea) = self.errores[i]
            lista_errores += ('ERROR linea ' + str(linea) + ': ' + cur_error)
            lista_errores += '\n'

        lista_warnings = ''
        for i in range(len(self.warnings)):
            (cur_warning, linea) = self.warnings[i]
            lista_warnings += ('WARNING linea ' + str(linea) + ': ' + cur_warning)
            lista_warnings += '\n'

        ret_value = lista_errores + lista_warnings
        return ret_value
