from nodo import Nodo


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")

    def coincidir(self, tipo_esperado):
        tipo, valor = self.actual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        else:
            print(
                f"Error: Se esperaba {tipo_esperado}, pero se encontró {tipo} ('{valor}'). ¿Olvidaste un punto y coma?")
            self.pos += 1  # Sigue adelante para intentar continuar el análisis
            return None

    def analizar(self):
        try:
            arbol = self.programa()
            print("Análisis completado. Generando árbol sintáctico...")
            return arbol
        except Exception as e:
            print(f"Error: {e}")
            return self.arbol_parcial if hasattr(self, "arbol_parcial") else None

    def programa(self):
        if self.actual()[1] != "establo":
            raise SyntaxError("El programa debe iniciar con 'establo'")

        self.coincidir("PALABRA_CLAVE")  # 'establo'
        nodo_programa = Nodo("programa", "establo")  # Nodo raíz del programa

        # Procesa las instrucciones
        nodo_instrucciones = self.instrucciones()
        nodo_programa.agregar_hijo(nodo_instrucciones)

        if self.actual()[1] != "fin_establo":
            raise SyntaxError("El programa debe finalizar con 'fin_establo'")
        self.coincidir("PALABRA_CLAVE")  # 'fin_establo'

        return nodo_programa

    def instrucciones(self):
        nodo_instrucciones = Nodo("instrucciones", "")
        while self.pos < len(self.tokens):
            tipo, valor = self.actual()

            # Condición de salida para evitar el bucle infinito
            if valor == "fin_establo":
                break

            nodo_instruccion = self.instruccion()
            if nodo_instruccion is None:
                break  # Si la instrucción no es válida, termina el bucle

            nodo_instrucciones.agregar_hijo(nodo_instruccion)
        return nodo_instrucciones

    def instruccion(self):
        tipo, valor = self.actual()

        if valor == "vaca":
            return self.declaracion()
        elif valor == "muu":
            return self.impresion()
        elif valor == "si":
            return self.condicional()
        elif valor == "mientras":
            return self.bucle_mientras()
        elif valor == "para":
            return self.bucle_para()
        elif valor == "fin_establo":
            return None  # Fin del programa
        elif tipo == "IDENTIFICADOR":
            return self.asignacion()
        else:
            raise SyntaxError(f"Instrucción no válida: '{valor}'")

    def declaracion(self):
        self.coincidir("PALABRA_CLAVE")  # 'vaca'
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        valor = self.expresion()
        self.coincidir("DELIMITADOR")  # ;

        nodo_declaracion = Nodo("declaracion", "vaca")
        nodo_declaracion.agregar_hijo(Nodo("identificador", nombre))
        nodo_declaracion.agregar_hijo(Nodo("valor", valor))
        return nodo_declaracion

    def asignacion(self):
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        valor = self.expresion()
        self.coincidir("DELIMITADOR")  # ;

        nodo_asignacion = Nodo("asignacion", "=")
        nodo_asignacion.agregar_hijo(Nodo("identificador", nombre))
        nodo_asignacion.agregar_hijo(Nodo("valor", valor))
        return nodo_asignacion

    def impresion(self):
        self.coincidir("PALABRA_CLAVE")  # 'muu'
        tipo, valor = self.actual()
        nodo_impresion = Nodo("impresion", "muu")

        if tipo == "CADENA":
            nodo_impresion.agregar_hijo(Nodo("cadena", valor))
            self.coincidir("CADENA")
        elif tipo == "IDENTIFICADOR":
            nodo_impresion.agregar_hijo(Nodo("identificador", valor))
            self.coincidir("IDENTIFICADOR")
        else:
            raise SyntaxError(
                f"Se esperaba una cadena o identificador después de 'muu', pero se encontró {tipo} ('{valor}').")

        self.coincidir("DELIMITADOR")  # ;
        return nodo_impresion

    def expresion(self):
        tipo, valor = self.actual()
        if tipo in ["NUMERO", "IDENTIFICADOR"]:
            self.pos += 1
            return valor
        else:
            raise SyntaxError(f"Expresión inválida: se esperaba número o variable, pero se encontró {tipo} ('{valor}')")

    def bucle_para(self):
        self.coincidir("PALABRA_CLAVE")  # 'para'
        self.coincidir("PALABRA_CLAVE")  # 'vaca'
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        inicio = self.expresion()
        self.coincidir("PALABRA_CLAVE")  # 'hasta'
        fin = self.expresion()
        self.coincidir("DELIMITADOR")  # ;

        nodo_bucle_para = Nodo("bucle_para", "para")
        nodo_bucle_para.agregar_hijo(Nodo("identificador", nombre))
        nodo_bucle_para.agregar_hijo(Nodo("inicio", inicio))
        nodo_bucle_para.agregar_hijo(Nodo("fin", fin))

        # Procesar las instrucciones dentro del bucle
        instrucciones_bucle = self.instrucciones()
        nodo_bucle_para.agregar_hijo(instrucciones_bucle)

        # Asegurarse de que se ha encontrado 'fin_para'
        if self.actual()[1] != "fin_para":
            raise SyntaxError("Se esperaba 'fin_para', pero no se encontró.")

        self.coincidir("PALABRA_CLAVE")  # 'fin_para'

        return nodo_bucle_para


# Función para imprimir el árbol sintáctico
def imprimir_arbol(nodo, nivel=0):
    if nodo is None:
        print("  " * nivel + "[Nodo nulo]")
        return
    indentacion = "  " * nivel
    print(f"{indentacion}{nodo.tipo}: {nodo.valor}")
    for hijo in nodo.hijos:
        imprimir_arbol(hijo, nivel + 1)
