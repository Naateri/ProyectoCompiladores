class Produccion:

    def __init__(self, texto):
        # Separar izquierda de derecha
        split_result = texto.split(':=')
        #print(split_result)
        self.left = split_result[0].strip()
        print(split_result)
        total_rules = split_result[1].split('|')
        self.right = [rule.strip() for rule in total_rules]

    def __str__(self):
        return self.left + ' := ' + str(self.right)
