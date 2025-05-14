class Nodo:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # El tipo de nodo (por ejemplo, "expresion", "instruccion")
        self.valor = valor  # El valor asociado al nodo (por ejemplo, el nombre de una variable o un número)
        self.hijos = []  # Lista de nodos hijos (subexpresiones o instrucciones)

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def __repr__(self):
        return f"{self.tipo}: {self.valor}"

