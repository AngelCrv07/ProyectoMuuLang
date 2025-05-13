from interpreter import interpreter


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.interpreter = interpreter()  # Instancia del intérprete

    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")

    def coincidir(self, tipo_esperado):
        tipo, valor = self.actual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        raise SyntaxError(f"Se esperaba {tipo_esperado}, pero se encontró {tipo} ('{valor}')")

    def analizar(self):
        self.programa()
        if self.pos < len(self.tokens):
            tipo, valor = self.actual()
            raise SyntaxError(f"Tokens inesperados después del fin del programa: {tipo} ('{valor}')")
        print("Análisis sintáctico completado sin errores.")

    def programa(self):
        if self.actual()[1] != "establo":
            raise SyntaxError("El programa debe iniciar con 'establo'")
        self.coincidir("PALABRA_CLAVE")  # 'establo'
        self.instrucciones()
        if self.actual()[1] != "fin_establo":
            raise SyntaxError("El programa debe finalizar con 'fin_establo'")
        self.coincidir("PALABRA_CLAVE")  # 'fin_establo'

    def instrucciones(self):
        while self.pos < len(self.tokens):
            tipo, valor = self.actual()
            if valor == "fin_establo":
                break
            self.instruccion()

    def instruccion(self):
        tipo, valor = self.actual()
        if valor == "vaca":
            self.declaracion()
        elif valor == "muu":
            self.impresion()
        elif valor == "si":
            self.condicional()
        elif valor == "mientras":
            self.bucle_mientras()
        elif valor == "para":
            self.bucle_para()
        elif tipo == "IDENTIFICADOR":
            self.asignacion()
        else:
            raise SyntaxError(f"Instrucción no válida: '{valor}'")

    def declaracion(self):
        self.coincidir("PALABRA_CLAVE")  # 'vaca'
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        valor = self.expresion()
        self.coincidir("DELIMITADOR")  # ;

        # Ejecutar la declaración con el intérprete
        self.interpreter.ejecutar(("ASIGNACION", (nombre, valor)))

    def asignacion(self):
        self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        valor = self.expresion()
        self.coincidir("DELIMITADOR")  # ;

        # Ejecutar la asignación con el intérprete
        self.interpreter.ejecutar(("ASIGNACION", (self.tokens[self.pos - 2][1], valor)))

    def impresion(self):
        self.coincidir("PALABRA_CLAVE")  # muu
        tipo, valor = self.actual()
        if tipo == "CADENA":
            self.coincidir("DELIMITADOR")  # ;
            self.interpreter.ejecutar(("IMPRIMIR", valor))
        elif tipo == "IDENTIFICADOR":
            # Si es identificador, imprimir el valor de la variable
            self.coincidir("DELIMITADOR")  # ;
            valor_variable = self.interpreter.obtener_variable(valor)
            self.interpreter.ejecutar(("IMPRIMIR", valor_variable))

    def expresion(self):
        tipo, valor = self.actual()
        if tipo in ["NUMERO", "IDENTIFICADOR"]:
            self.pos += 1  # Avanzar
            return valor
        else:
            raise SyntaxError(f"Expresión inválida: se esperaba número o variable, pero se encontró {tipo} ('{valor}')")

        self.pos += 1  # Avanza sobre el primer operando

        while self.actual()[0] == "OPERADOR":
            self.pos += 1  # Consumir operador
            tipo2, valor2 = self.actual()
            if tipo2 not in ["NUMERO", "IDENTIFICADOR"]:
                raise SyntaxError(
                    f"Después del operador se esperaba número o variable, pero se encontró {tipo2} ('{valor2}')")
            self.pos += 1  # Consumir operando

    def bucle_mientras(self):
        self.coincidir("PALABRA_CLAVE")  # "mientras"
        self.condicion()  # Condición de la sentencia 'mientras'
        while self.actual()[1] != "fin_mientras":
            self.instruccion()
        self.coincidir("PALABRA_CLAVE")  # 'fin_mientras'

    def condicion(self):
        self.coincidir("IDENTIFICADOR")
        self.coincidir("OPERADOR")
        tipo, _ = self.actual()
        if tipo not in ["NUMERO", "IDENTIFICADOR"]:
            raise SyntaxError("Condición inválida: se esperaba número o variable.")
        self.pos += 1

    def bucle_para(self):
        self.coincidir("PALABRA_CLAVE")  # para
        self.coincidir("PALABRA_CLAVE")  # vaca
        self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        self.expresion()
        if self.actual()[1] != "hasta":
            raise SyntaxError("Se esperaba 'hasta' en bucle para.")
        self.coincidir("PALABRA_CLAVE")  # hasta
        self.expresion()
        while self.actual()[1] != "fin_para":
            self.instruccion()
        self.coincidir("PALABRA_CLAVE")
