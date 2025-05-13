class interpreter:
    def __init__(self):
        self.variables = {}

    def ejecutar(self, instruccion):
        tipo, valor = instruccion
        if tipo == "ASIGNACION":
            nombre, expresion = valor
            self.variables[nombre] = expresion
        elif tipo == "IMPRIMIR":
            print(valor)
        else:
            raise SyntaxError(f"Operación no soportada: {tipo}")

    def obtener_variable(self, nombre):
        return self.variables.get(nombre, None)
